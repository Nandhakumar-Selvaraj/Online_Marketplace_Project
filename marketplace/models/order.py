"""
models/order.py
───────────────
Cart model  — add/remove/view items before checkout.
Order model — place & view orders.
"""

from db.connection import get_connection


class Cart:
    # ── Add item to cart ─────────────────────────────────────────────────────
    @staticmethod
    def add_item(buyer_id, product_id, quantity=1):
        conn = get_connection()
        cursor = conn.cursor()
        # If item already in cart, increase quantity
        cursor.execute(
            "SELECT id, quantity FROM cart WHERE buyer_id=%s AND product_id=%s",
            (buyer_id, product_id)
        )
        row = cursor.fetchone()
        if row:
            cursor.execute(
                "UPDATE cart SET quantity=%s WHERE id=%s",
                (row[1] + quantity, row[0])
            )
        else:
            cursor.execute(
                "INSERT INTO cart (buyer_id, product_id, quantity) VALUES (%s,%s,%s)",
                (buyer_id, product_id, quantity)
            )
        conn.commit()
        cursor.close()
        conn.close()

    # ── View cart items ──────────────────────────────────────────────────────
    @staticmethod
    def get_items(buyer_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id AS cart_id, p.id AS product_id, p.name,
                   p.price, c.quantity,
                   (p.price * c.quantity) AS subtotal
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.buyer_id = %s
        """, (buyer_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # ── Remove one item ──────────────────────────────────────────────────────
    @staticmethod
    def remove_item(cart_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id=%s", (cart_id,))
        conn.commit()
        cursor.close()
        conn.close()

    # ── Clear entire cart after checkout ────────────────────────────────────
    @staticmethod
    def clear(buyer_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE buyer_id=%s", (buyer_id,))
        conn.commit()
        cursor.close()
        conn.close()


class Order:
    # ── Place order (checkout all cart items) ────────────────────────────────
    @staticmethod
    def checkout(buyer_id):
        """
        Converts every cart item into an order row,
        reduces stock, then clears the cart.
        """
        items = Cart.get_items(buyer_id)
        if not items:
            raise ValueError("Cart is empty.")

        conn = get_connection()
        cursor = conn.cursor()
        for item in items:
            # Check stock
            cursor.execute("SELECT stock FROM products WHERE id=%s", (item["product_id"],))
            stock = cursor.fetchone()[0]
            if stock < item["quantity"]:
                raise ValueError(f"Not enough stock for '{item['name']}'.")

            # Insert order
            cursor.execute(
                """INSERT INTO orders (buyer_id, product_id, quantity, total_price)
                   VALUES (%s,%s,%s,%s)""",
                (buyer_id, item["product_id"], item["quantity"], item["subtotal"])
            )
            # Reduce stock
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id=%s",
                (item["quantity"], item["product_id"])
            )

        conn.commit()
        cursor.close()
        conn.close()
        Cart.clear(buyer_id)

    # ── View buyer's orders ──────────────────────────────────────────────────
    @staticmethod
    def get_buyer_orders(buyer_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.id, p.name AS product, o.quantity,
                   o.total_price, o.status, o.ordered_at
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.buyer_id = %s
            ORDER BY o.ordered_at DESC
        """, (buyer_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # ── View orders for seller's products ───────────────────────────────────
    @staticmethod
    def get_seller_orders(seller_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.id, p.name AS product, u.name AS buyer,
                   o.quantity, o.total_price, o.status, o.ordered_at
            FROM orders o
            JOIN products p ON o.product_id = p.id
            JOIN users   u ON o.buyer_id    = u.id
            WHERE p.seller_id = %s
            ORDER BY o.ordered_at DESC
        """, (seller_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # ── Update order status (seller confirms/cancels) ────────────────────────
    @staticmethod
    def update_status(order_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status=%s WHERE id=%s",
            (status, order_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
