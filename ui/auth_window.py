import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User


class AuthWindow:
    def __init__(self, on_success):
        """
        on_success: callback function called with a User object after login.
        This lets main.py open the correct dashboard without AuthWindow
        knowing anything about what comes next (good OOP separation).
        """
        self.on_success = on_success

        self.root = tk.Tk()
        self.root.title("🛒 Online Marketplace — Login")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self._build_ui()

    # ── Build the tabbed UI ──────────────────────────────────────────────────
    def _build_ui(self):
        # Title label
        tk.Label(
            self.root, text="🛒 Online Marketplace",
            font=("Georgia", 18, "bold"),
            bg="#1a1a2e", fg="#e94560"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Buy & Sell with ease",
            font=("Arial", 10), bg="#1a1a2e", fg="#a8a8b3"
        ).pack(pady=(0, 15))

        # Notebook for Login / Register tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#16213e", foreground="#a8a8b3",
                         padding=[20, 8], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "#e94560")],
                  foreground=[("selected", "white")])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=20, pady=5)

        # ── Login Tab ────────────────────────────────────────────────────────
        login_frame = tk.Frame(nb, bg="#16213e")
        nb.add(login_frame, text="  Login  ")
        self._build_login_tab(login_frame)

        # ── Register Tab ─────────────────────────────────────────────────────
        reg_frame = tk.Frame(nb, bg="#16213e")
        nb.add(reg_frame, text="  Register  ")
        self._build_register_tab(reg_frame)

    # ── Helper: styled label + entry pair ────────────────────────────────────
    def _field(self, parent, label, show=None):
        tk.Label(parent, text=label, bg="#16213e", fg="#a8a8b3",
                 font=("Arial", 10), anchor="w").pack(fill="x", padx=30, pady=(10,2))
        var = tk.StringVar()
        entry = tk.Entry(parent, textvariable=var, show=show,
                         bg="#0f3460", fg="white", insertbackground="white",
                         relief="flat", font=("Arial", 11), bd=8)
        entry.pack(fill="x", padx=30)
        return var

    # ── Login tab content ─────────────────────────────────────────────────────
    def _build_login_tab(self, frame):
        self.login_email    = self._field(frame, "Email")
        self.login_password = self._field(frame, "Password", show="*")

        tk.Button(
            frame, text="Login →",
            command=self._do_login,
            bg="#e94560", fg="white", font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2", pady=8
        ).pack(fill="x", padx=30, pady=20)

    # ── Register tab content ──────────────────────────────────────────────────
    def _build_register_tab(self, frame):
        self.reg_name     = self._field(frame, "Full Name")
        self.reg_email    = self._field(frame, "Email")
        self.reg_password = self._field(frame, "Password", show="*")

        # Role selector (Buyer / Seller)
        tk.Label(frame, text="Register as", bg="#16213e", fg="#a8a8b3",
                 font=("Arial", 10), anchor="w").pack(fill="x", padx=30, pady=(10,2))
        self.reg_role = tk.StringVar(value="buyer")
        role_frame = tk.Frame(frame, bg="#16213e")
        role_frame.pack(fill="x", padx=30)
        for role in ("buyer", "seller"):
            tk.Radiobutton(
                role_frame, text=role.capitalize(), variable=self.reg_role,
                value=role, bg="#16213e", fg="white", selectcolor="#0f3460",
                activebackground="#16213e", font=("Arial", 10)
            ).pack(side="left", padx=10)

        tk.Button(
            frame, text="Create Account →",
            command=self._do_register,
            bg="#e94560", fg="white", font=("Arial", 11, "bold"),
            relief="flat", cursor="hand2", pady=8
        ).pack(fill="x", padx=30, pady=15)

    # ── Login logic ──────────────────────────────────────────────────────────
    def _do_login(self):
        email    = self.login_email.get().strip()
        password = self.login_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Missing", "Please fill all fields.")
            return

        user = User.login(email, password)
        if user:
            self.root.destroy()          # close login window
            self.on_success(user)        # hand control to main.py
        else:
            messagebox.showerror("Failed", "Invalid email or password.")

    # ── Register logic ────────────────────────────────────────────────────────
    def _do_register(self):
        name     = self.reg_name.get().strip()
        email    = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        role     = self.reg_role.get()

        if not all([name, email, password]):
            messagebox.showwarning("Missing", "Please fill all fields.")
            return
        if len(password) < 6:
            messagebox.showwarning("Weak", "Password must be at least 6 characters.")
            return

        try:
            User.register(name, email, password, role)
            messagebox.showinfo("Success", f"Account created! Please login as {role}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()
