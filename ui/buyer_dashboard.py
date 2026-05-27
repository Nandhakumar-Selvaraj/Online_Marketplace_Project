import tkinter as tk
from tkinter import ttk, messagebox
from models.product import Product
from models.order   import Cart, Order


class BuyerDashboard:
    def __init__(self, user):
        self.user = user   # logged-in User object

        self.root = tk.Tk()
        self.root.title(f"🛒 Marketplace — Buyer: {user.name}")
        self.root.geometry("900x580")
        self.root.configure(bg="#1a1a2e")

        self._build_ui()
        self._load_products()

    # ── Top header bar ────────────────────────────────────────────────────────
    def _build_ui(self):
        header = tk.Frame(self.root, bg="#e94560", pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"👤 {self.user.name}  |  Buyer Dashboard",
                 font=("Georgia", 14, "bold"), bg="#e94560", fg="white").pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self._logout,
                  bg="#c0392b", fg="white", relief="flat", cursor="hand2",
                  font=("Arial", 10)).pack(side="right", padx=20)

        # Notebook tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1a1a2e")
        style.configure("TNotebook.Tab", background="#16213e", foreground="#a8a8b3",
                         padding=[18, 7], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected","#e94560")],
                  foreground=[("selected","white")])
        style.configure("Treeview", background="#16213e", foreground="white",
                         fieldbackground="#16213e", rowheight=28)
        style.configure("Treeview.Heading", background="#0f3460", foreground="white",
                         font=("Arial", 10, "bold"))

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab frames
        browse_frame = tk.Frame(nb, bg="#16213e")
        cart_frame   = tk.Frame(nb, bg="#16213e")
        orders_frame = tk.Frame(nb, bg="#16213e")

        nb.add(browse_frame, text="  🛍 Browse Products  ")
        nb.add(cart_frame,   text="  🛒 My Cart  ")
        nb.add(orders_frame, text="  📦 My Orders  ")

        nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self._build_browse(browse_frame)
        self._build_cart(cart_frame)
        self._build_orders(orders_frame)

    # ── TAB 1: Browse products ────────────────────────────────────────────────
    def _build_browse(self, frame):
        cols = ("ID","Product","Seller","Price","Stock")
        self.browse_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.browse_tree.heading(col, text=col)
        self.browse_tree.column("ID",      width=50,  anchor="center")
        self.browse_tree.column("Product", width=250)
        self.browse_tree.column("Seller",  width=150)
        self.browse_tree.column("Price",   width=100, anchor="center")
        self.browse_tree.column("Stock",   width=80,  anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.browse_tree.yview)
        self.browse_tree.configure(yscrollcommand=sb.set)
        self.browse_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="left", fill="y", pady=10)

        # Right side controls
        ctrl = tk.Frame(frame, bg="#16213e", padx=10)
        ctrl.pack(side="left", fill="y", pady=10)

        tk.Label(ctrl, text="Quantity:", bg="#16213e", fg="#a8a8b3",
                 font=("Arial",10)).pack(pady=(20,4))
        self.qty_var = tk.IntVar(value=1)
        tk.Spinbox(ctrl, from_=1, to=50, textvariable=self.qty_var,
                   width=5, font=("Arial",11)).pack()

        tk.Button(ctrl, text="Add to Cart 🛒",
                  command=self._add_to_cart,
                  bg="#e94560", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",11,"bold"), pady=10,
                  width=14).pack(pady=20)

        tk.Button(ctrl, text="🔄 Refresh",
                  command=self._load_products,
                  bg="#0f3460", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",10)).pack()

    # ── TAB 2: Cart ───────────────────────────────────────────────────────────
    def _build_cart(self, frame):
        cols = ("CartID","Product","Price","Qty","Subtotal")
        self.cart_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.cart_tree.heading(col, text=col)
        self.cart_tree.column("CartID",  width=60, anchor="center")
        self.cart_tree.column("Product", width=250)
        self.cart_tree.column("Price",   width=100, anchor="center")
        self.cart_tree.column("Qty",     width=80,  anchor="center")
        self.cart_tree.column("Subtotal",width=100, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=sb.set)
        self.cart_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="left", fill="y", pady=10)

        ctrl = tk.Frame(frame, bg="#16213e", padx=10)
        ctrl.pack(side="left", fill="y", pady=10)

        self.total_label = tk.Label(ctrl, text="Total: ₹0.00",
                                    bg="#16213e", fg="#e94560",
                                    font=("Arial",13,"bold"))
        self.total_label.pack(pady=20)

        tk.Button(ctrl, text="Remove Item ❌",
                  command=self._remove_from_cart,
                  bg="#c0392b", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",10), pady=8, width=14).pack(pady=5)

        tk.Button(ctrl, text="✅ Checkout",
                  command=self._checkout,
                  bg="#27ae60", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",12,"bold"), pady=10, width=14).pack(pady=15)

    # ── TAB 3: Orders ─────────────────────────────────────────────────────────
    def _build_orders(self, frame):
        cols = ("OrderID","Product","Qty","Total","Status","Date")
        self.orders_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.orders_tree.heading(col, text=col)
        self.orders_tree.column("OrderID", width=70,  anchor="center")
        self.orders_tree.column("Product", width=220)
        self.orders_tree.column("Qty",     width=60,  anchor="center")
        self.orders_tree.column("Total",   width=100, anchor="center")
        self.orders_tree.column("Status",  width=100, anchor="center")
        self.orders_tree.column("Date",    width=160)

        # Colour rows by status
        self.orders_tree.tag_configure("pending",   background="#2d2d16")
        self.orders_tree.tag_configure("confirmed", background="#1a2d1a")
        self.orders_tree.tag_configure("cancelled", background="#2d1a1a")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=sb.set)
        self.orders_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="left", fill="y", pady=10)

    # ── Data loaders ──────────────────────────────────────────────────────────
    def _load_products(self):
        self.browse_tree.delete(*self.browse_tree.get_children())
        for p in Product.get_all():
            self.browse_tree.insert("", "end", values=(
                p["id"], p["name"], p["seller_name"],
                f"₹{p['price']:.2f}", p["stock"]
            ))

    def _load_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        items = Cart.get_items(self.user.id)
        total = sum(float(i["subtotal"]) for i in items)
        for i in items:
            self.cart_tree.insert("", "end", values=(
                i["cart_id"], i["name"],
                f"₹{float(i['price']):.2f}",
                i["quantity"],
                f"₹{float(i['subtotal']):.2f}"
            ))
        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def _load_orders(self):
        self.orders_tree.delete(*self.orders_tree.get_children())
        for o in Order.get_buyer_orders(self.user.id):
            self.orders_tree.insert("", "end", tag=o["status"], values=(
                o["id"], o["product"], o["quantity"],
                f"₹{float(o['total_price']):.2f}",
                o["status"].upper(), str(o["ordered_at"])[:16]
            ))

    def _on_tab_change(self, event):
        tab = event.widget.index("current")
        if tab == 1: self._load_cart()
        if tab == 2: self._load_orders()

    # ── Actions ───────────────────────────────────────────────────────────────
    def _add_to_cart(self):
        sel = self.browse_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a product first.")
            return
        product_id = self.browse_tree.item(sel[0])["values"][0]
        qty = self.qty_var.get()
        Cart.add_item(self.user.id, product_id, qty)
        messagebox.showinfo("Added", "Item added to cart!")

    def _remove_from_cart(self):
        sel = self.cart_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an item to remove.")
            return
        cart_id = self.cart_tree.item(sel[0])["values"][0]
        Cart.remove_item(cart_id)
        self._load_cart()

    def _checkout(self):
        if not messagebox.askyesno("Confirm", "Place order for all cart items?"):
            return
        try:
            Order.checkout(self.user.id)
            messagebox.showinfo("Success", "🎉 Order placed successfully!")
            self._load_cart()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _logout(self):
        self.root.destroy()
        # Re-import here to avoid circular import at module load time
        from ui.auth_window import AuthWindow
        import main
        AuthWindow(main.on_login).run()

    def run(self):
        self.root.mainloop()
