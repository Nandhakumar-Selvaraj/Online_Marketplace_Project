import tkinter as tk
from tkinter import ttk, messagebox
from models.product import Product
from models.order   import Order


class SellerDashboard:
    def __init__(self, user):
        self.user = user

        self.root = tk.Tk()
        self.root.title(f"🛒 Marketplace — Seller: {user.name}")
        self.root.geometry("960x600")
        self.root.configure(bg="#1a1a2e")

        self._build_ui()
        self._load_products()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_ui(self):
        header = tk.Frame(self.root, bg="#27ae60", pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"🏪 {self.user.name}  |  Seller Dashboard",
                 font=("Georgia",14,"bold"), bg="#27ae60", fg="white").pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self._logout,
                  bg="#1e8449", fg="white", relief="flat", cursor="hand2",
                  font=("Arial",10)).pack(side="right", padx=20)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",     background="#1a1a2e")
        style.configure("TNotebook.Tab", background="#16213e", foreground="#a8a8b3",
                         padding=[18,7], font=("Arial",10))
        style.map("TNotebook.Tab", background=[("selected","#27ae60")],
                  foreground=[("selected","white")])
        style.configure("Treeview", background="#16213e", foreground="white",
                         fieldbackground="#16213e", rowheight=28)
        style.configure("Treeview.Heading", background="#0f3460", foreground="white",
                         font=("Arial",10,"bold"))

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=15, pady=10)

        prod_frame   = tk.Frame(nb, bg="#16213e")
        orders_frame = tk.Frame(nb, bg="#16213e")
        nb.add(prod_frame,   text="  📦 My Products  ")
        nb.add(orders_frame, text="  📋 Incoming Orders  ")
        nb.bind("<<NotebookTabChanged>>", lambda e: self._load_orders()
                if nb.index("current") == 1 else None)

        self._build_products_tab(prod_frame)
        self._build_orders_tab(orders_frame)

    # ── TAB 1: Products ───────────────────────────────────────────────────────
    def _build_products_tab(self, frame):
        # Left: Treeview
        cols = ("ID","Name","Price","Stock","Description")
        self.prod_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.prod_tree.heading(col, text=col)
        self.prod_tree.column("ID",          width=50,  anchor="center")
        self.prod_tree.column("Name",        width=200)
        self.prod_tree.column("Price",       width=90,  anchor="center")
        self.prod_tree.column("Stock",       width=70,  anchor="center")
        self.prod_tree.column("Description", width=260)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.prod_tree.yview)
        self.prod_tree.configure(yscrollcommand=sb.set)
        self.prod_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="left", fill="y", pady=10)
        self.prod_tree.bind("<<TreeviewSelect>>", self._on_product_select)

        # Right: Form panel
        form = tk.Frame(frame, bg="#0f3460", padx=15, pady=15)
        form.pack(side="left", fill="y", pady=10, padx=10)

        tk.Label(form, text="Product Details", font=("Georgia",12,"bold"),
                 bg="#0f3460", fg="white").grid(row=0, column=0, columnspan=2, pady=(0,10))

        labels = ["Name", "Description", "Price (₹)", "Stock"]
        self.form_vars = {}
        for i, lbl in enumerate(labels, start=1):
            tk.Label(form, text=lbl+":", bg="#0f3460", fg="#a8a8b3",
                     font=("Arial",10)).grid(row=i, column=0, sticky="w", pady=4)
            var = tk.StringVar()
            widget = (tk.Text(form, height=3, width=22, bg="#16213e", fg="white",
                               insertbackground="white", relief="flat", font=("Arial",10))
                      if lbl == "Description"
                      else tk.Entry(form, textvariable=var, width=22,
                                    bg="#16213e", fg="white", insertbackground="white",
                                    relief="flat", font=("Arial",10), bd=5))
            widget.grid(row=i, column=1, pady=4, padx=(5,0))
            self.form_vars[lbl] = (var, widget)

        # Buttons
        btn_cfg = dict(relief="flat", cursor="hand2", font=("Arial",10,"bold"),
                       pady=7, width=12)
        tk.Button(form, text="➕ Add",    command=self._add_product,
                  bg="#27ae60", fg="white", **btn_cfg).grid(row=6, column=0, pady=(15,5))
        tk.Button(form, text="✏️ Update", command=self._update_product,
                  bg="#f39c12", fg="white", **btn_cfg).grid(row=6, column=1, pady=(15,5))
        tk.Button(form, text="🗑 Delete", command=self._delete_product,
                  bg="#c0392b", fg="white", **btn_cfg).grid(row=7, column=0, pady=5)
        tk.Button(form, text="🔄 Clear",  command=self._clear_form,
                  bg="#555", fg="white", **btn_cfg).grid(row=7, column=1, pady=5)

        self.selected_product_id = None

    # ── TAB 2: Orders ─────────────────────────────────────────────────────────
    def _build_orders_tab(self, frame):
        cols = ("OrderID","Product","Buyer","Qty","Total","Status","Date")
        self.orders_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.orders_tree.heading(col, text=col)
        widths = [70,180,130,60,90,100,140]
        for col, w in zip(cols, widths):
            self.orders_tree.column(col, width=w, anchor="center" if w<160 else "w")

        self.orders_tree.tag_configure("pending",   background="#2d2d16")
        self.orders_tree.tag_configure("confirmed", background="#1a2d1a")
        self.orders_tree.tag_configure("cancelled", background="#2d1a1a")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=sb.set)
        self.orders_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="left", fill="y", pady=10)

        ctrl = tk.Frame(frame, bg="#16213e", padx=10)
        ctrl.pack(side="left", fill="y", pady=10)

        tk.Label(ctrl, text="Update Status:", bg="#16213e", fg="#a8a8b3",
                 font=("Arial",10)).pack(pady=(30,5))
        self.status_var = tk.StringVar(value="confirmed")
        for s in ("confirmed","cancelled"):
            tk.Radiobutton(ctrl, text=s.capitalize(), variable=self.status_var,
                           value=s, bg="#16213e", fg="white",
                           selectcolor="#0f3460", font=("Arial",10)).pack(pady=3)

        tk.Button(ctrl, text="Update Status ✅",
                  command=self._update_order_status,
                  bg="#27ae60", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",10,"bold"),
                  pady=8, width=16).pack(pady=20)

        tk.Button(ctrl, text="🔄 Refresh",
                  command=self._load_orders,
                  bg="#0f3460", fg="white", relief="flat",
                  cursor="hand2", font=("Arial",10)).pack()

    # ── Data loaders ──────────────────────────────────────────────────────────
    def _load_products(self):
        self.prod_tree.delete(*self.prod_tree.get_children())
        for p in Product.get_by_seller(self.user.id):
            self.prod_tree.insert("", "end", iid=str(p["id"]), values=(
                p["id"], p["name"],
                f"₹{float(p['price']):.2f}",
                p["stock"], p["description"]
            ))

    def _load_orders(self):
        self.orders_tree.delete(*self.orders_tree.get_children())
        for o in Order.get_seller_orders(self.user.id):
            self.orders_tree.insert("", "end", tag=o["status"], values=(
                o["id"], o["product"], o["buyer"], o["quantity"],
                f"₹{float(o['total_price']):.2f}",
                o["status"].upper(), str(o["ordered_at"])[:16]
            ))

    # ── Form helpers ──────────────────────────────────────────────────────────
    def _get_form(self):
        """Read all form fields and return a dict."""
        data = {}
        for key, (var, widget) in self.form_vars.items():
            if isinstance(widget, tk.Text):
                data[key] = widget.get("1.0", "end").strip()
            else:
                data[key] = var.get().strip()
        return data

    def _clear_form(self):
        for key, (var, widget) in self.form_vars.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            else:
                var.set("")
        self.selected_product_id = None

    def _on_product_select(self, event):
        """Populate form when a product row is clicked."""
        sel = self.prod_tree.selection()
        if not sel: return
        vals = self.prod_tree.item(sel[0])["values"]
        self.selected_product_id = vals[0]
        fields = {"Name": vals[1], "Price (₹)": str(vals[2]).replace("₹",""),
                  "Stock": str(vals[3]), "Description": vals[4]}
        for key, (var, widget) in self.form_vars.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0","end")
                widget.insert("1.0", fields.get(key,""))
            else:
                var.set(fields.get(key,""))

    # ── CRUD actions ──────────────────────────────────────────────────────────
    def _add_product(self):
        d = self._get_form()
        if not d["Name"] or not d["Price (₹)"] or not d["Stock"]:
            messagebox.showwarning("Missing", "Name, Price and Stock are required.")
            return
        try:
            Product.add(self.user.id, d["Name"], d["Description"],
                        float(d["Price (₹)"]), int(d["Stock"]))
            self._load_products()
            self._clear_form()
            messagebox.showinfo("Done", "Product added!")
        except ValueError:
            messagebox.showerror("Error", "Price must be a number; Stock must be an integer.")

    def _update_product(self):
        if not self.selected_product_id:
            messagebox.showwarning("Select", "Select a product to update.")
            return
        d = self._get_form()
        try:
            Product.update(self.selected_product_id, d["Name"], d["Description"],
                           float(d["Price (₹)"]), int(d["Stock"]))
            self._load_products()
            messagebox.showinfo("Done", "Product updated!")
        except ValueError:
            messagebox.showerror("Error", "Price must be a number; Stock must be integer.")

    def _delete_product(self):
        if not self.selected_product_id:
            messagebox.showwarning("Select", "Select a product to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete this product?"):
            Product.delete(self.selected_product_id)
            self._load_products()
            self._clear_form()

    def _update_order_status(self):
        sel = self.orders_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an order first.")
            return
        order_id = self.orders_tree.item(sel[0])["values"][0]
        Order.update_status(order_id, self.status_var.get())
        self._load_orders()
        messagebox.showinfo("Updated", "Order status updated!")

    def _logout(self):
        self.root.destroy()
        from ui.auth_window import AuthWindow
        import main
        AuthWindow(main.on_login).run()

    def run(self):
        self.root.mainloop()
