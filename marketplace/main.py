"""
main.py  ←  RUN THIS FILE IN PYCHARM
─────────────────────────────────────────────────────────────────────────────
Online Marketplace — Entry point

Flow:
  1. initialize_db()   → creates DB + tables if they don't exist
  2. AuthWindow opens  → user logs in or registers
  3. on_login()        → routes to BuyerDashboard or SellerDashboard
─────────────────────────────────────────────────────────────────────────────
"""

import sys
import os

# ── Make sure Python can find our sub-packages ───────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from db.connection    import initialize_db
from ui.auth_window   import AuthWindow


def on_login(user):
    """
    Called by AuthWindow after a successful login.
    Routes the user to the correct dashboard based on their role.
    """
    if user.role == "buyer":
        from ui.buyer_dashboard  import BuyerDashboard
        BuyerDashboard(user).run()
    else:
        from ui.seller_dashboard import SellerDashboard
        SellerDashboard(user).run()


if __name__ == "__main__":
    print("🚀 Starting Online Marketplace...")
    initialize_db()              # Step 1 — ensure DB + tables exist
    AuthWindow(on_login).run()   # Step 2 — open login window
