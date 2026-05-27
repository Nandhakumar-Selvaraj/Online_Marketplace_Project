"""
models/product.py
─────────────────
Product model — CRUD operations for the products table.
"""

from db.connection import get_connection


class Product:
    def __init__(self, id, seller_id, name, description, price, stock):
        self.id          = id
        self.seller_id   = seller_id
        self.name        = name
        self.description = description
        self.price       = float(price)
        self.stock       = int(stock)

    # ── Add a new product (seller only) ─────────────────────────────────────
    @classmethod
    def add(cls, seller_id, name, description, price, stock):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (seller_id,name,description,price,stock) VALUES (%s,%s,%s,%s,%s)",
            (seller_id, name, description, price, stock)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return cls(new_id, seller_id, name, description, price, stock)

    # ── Fetch all products (buyer browse) ────────────────────────────────────
    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, u.name AS seller_name
            FROM products p
            JOIN users u ON p.seller_id = u.id
            WHERE p.stock > 0
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows   # list of dicts — easy to display in Treeview

    # ── Fetch products by seller ─────────────────────────────────────────────
    @classmethod
    def get_by_seller(cls, seller_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM products WHERE seller_id=%s ORDER BY created_at DESC",
            (seller_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # ── Update a product ─────────────────────────────────────────────────────
    @classmethod
    def update(cls, product_id, name, description, price, stock):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s, stock=%s WHERE id=%s",
            (name, description, price, stock, product_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    # ── Delete a product ─────────────────────────────────────────────────────
    @classmethod
    def delete(cls, product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
