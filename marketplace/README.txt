============================================================
   ONLINE MARKETPLACE — Python Desktop App
   Built with: Python + Tkinter + MySQL + OOP
============================================================

PROJECT STRUCTURE
─────────────────
marketplace/
├── main.py                  ← RUN THIS FILE
├── requirements.txt         ← Python packages needed
├── README.txt               ← This file
│
├── db/
│   ├── __init__.py
│   └── connection.py        ← MySQL connection + table creation
│
├── models/
│   ├── __init__.py
│   ├── user.py              ← Login, Register (OOP)
│   ├── product.py           ← Product CRUD (OOP)
│   └── order.py             ← Cart & Orders (OOP)
│
└── ui/
    ├── __init__.py
    ├── auth_window.py       ← Login / Register screen
    ├── buyer_dashboard.py   ← Buyer: Browse, Cart, Orders
    └── seller_dashboard.py  ← Seller: Products, Incoming Orders


============================================================
STEP-BY-STEP SETUP INSTRUCTIONS
============================================================

──────────────────────────────────────────────────────────
STEP 1 — Install Python
──────────────────────────────────────────────────────────
• Download Python 3.9 or above from: https://www.python.org/downloads/
• During installation, CHECK the box "Add Python to PATH"
• Verify install: open CMD and type:
      python --version
  You should see: Python 3.x.x

──────────────────────────────────────────────────────────
STEP 2 — Install MySQL
──────────────────────────────────────────────────────────
• Download MySQL Community Server from:
  https://dev.mysql.com/downloads/mysql/
• Install with default settings
• Set a ROOT PASSWORD during setup — remember it!
• Verify: open MySQL Command Line Client and login

──────────────────────────────────────────────────────────
STEP 3 — Install PyCharm (IDE)
──────────────────────────────────────────────────────────
• Download PyCharm Community (free) from:
  https://www.jetbrains.com/pycharm/download/
• Install with default settings

──────────────────────────────────────────────────────────
STEP 4 — Install Python Package (mysql-connector)
──────────────────────────────────────────────────────────
• Open PyCharm Terminal (bottom of screen) OR open CMD
• Run this command:

      pip install mysql-connector-python

• Wait for installation to complete
• You should see: Successfully installed mysql-connector-python

──────────────────────────────────────────────────────────
STEP 5 — Configure Your MySQL Password
──────────────────────────────────────────────────────────
• Open the file:  marketplace/db/connection.py
• Find this section at the top:

      DB_CONFIG = {
          "host": "localhost",
          "user": "root",
          "password": "yourpassword",   ← CHANGE THIS
          "database": "marketplace_db"
      }

• Replace "yourpassword" with your actual MySQL root password
• Save the file (Ctrl+S)

  EXAMPLE — if your password is "mysql123":
      "password": "mysql123",

──────────────────────────────────────────────────────────
STEP 6 — Open Project in PyCharm
──────────────────────────────────────────────────────────
• Open PyCharm
• Click: File → Open
• Browse to and select the "marketplace" folder
• Click OK / Open

──────────────────────────────────────────────────────────
STEP 7 — Run the Project
──────────────────────────────────────────────────────────
• In PyCharm, find "main.py" in the left panel
• Right-click on main.py → "Run 'main'"
  OR
• Open main.py and press the green ▶ Play button (top right)

• In the console you will see:
      ✅ Database and tables ready.

• The LOGIN WINDOW will open automatically!

──────────────────────────────────────────────────────────
STEP 8 — Use the Application
──────────────────────────────────────────────────────────

  FIRST TIME — Register accounts:
  1. Click the "Register" tab
  2. Enter Name, Email, Password
  3. Select role: Buyer or Seller
  4. Click "Create Account"
  5. Register at least one Buyer AND one Seller account

  AS A SELLER:
  1. Login with seller account
  2. Go to "My Products" tab
  3. Fill in product Name, Description, Price, Stock
  4. Click "Add" to list the product
  5. Check "Incoming Orders" tab to manage orders

  AS A BUYER:
  1. Login with buyer account
  2. "Browse Products" tab — see all listed products
  3. Select a product, set quantity, click "Add to Cart"
  4. Go to "My Cart" tab — review items and click "Checkout"
  5. "My Orders" tab — see order history and status


============================================================
WHAT HAPPENS AUTOMATICALLY ON FIRST RUN
============================================================
• The app creates a MySQL database called "marketplace_db"
• It creates 4 tables automatically:
    - users    (stores buyer & seller accounts)
    - products (stores product listings)
    - cart     (stores temporary cart items)
    - orders   (stores placed orders)
• You do NOT need to write any SQL manually


============================================================
TROUBLESHOOTING
============================================================

Problem: "mysql.connector not found" error
Fix: Run in terminal:  pip install mysql-connector-python

Problem: "MySQL connection failed" error
Fix: Check your password in db/connection.py
     Make sure MySQL server is running
     Open MySQL Workbench and check if server is ON

Problem: "No module named 'tkinter'" error
Fix: Tkinter is built into Python. Reinstall Python from python.org
     Make sure you download the standard installer (not minimal)

Problem: Window opens but shows no products
Fix: Login as a Seller first and add some products
     Then login as a Buyer to browse them

Problem: PyCharm shows "unresolved import" warnings
Fix: Go to File → Settings → Project → Python Interpreter
     Make sure the correct Python is selected
     Click + and install mysql-connector-python


============================================================
TECHNOLOGY SUMMARY
============================================================
Language  : Python 3.9+
UI        : Tkinter (ttk.Notebook, ttk.Treeview, messagebox)
Database  : MySQL (via mysql-connector-python)
OOP Used  : class, __init__, @classmethod, @staticmethod,
            encapsulation, callback pattern
No APIs   : 100% pure Python desktop application


============================================================
FILES YOU NEED TO MODIFY (only one!)
============================================================
  db/connection.py  →  line 14:  "password": "yourpassword"
  Change "yourpassword" to your MySQL root password.
  That's it. Everything else works automatically.

============================================================
