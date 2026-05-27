"""
db/connection.py
────────────────
Handles MySQL connection and creates all tables on first run.
Uses mysql-connector-python  →  pip install mysql-connector-python
"""
import mysql.connector
from mysql.connector import Error

# ── Change these to match your MySQL setup ──────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # your MySQL username
    "password": "sjn.1925",  # your MySQL password
    "database": "marketplace_db"
}
# ────────────────────────────────────────────────────────────────────────────

def get_connection():
    """Return a live MySQL connection object."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(f"MySQL connection failed: {e}")


def initialize_db():
    """
    Creates the database (if missing) and all required tables.
    Call this ONCE when the app starts (main.py does this).
    """
    # Step 1: Connect without selecting a database so we can CREATE it
    config_no_db = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**config_no_db)
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.execute(f"USE {DB_CONFIG['database']}")

    # ── Users table (buyers & sellers share one table, role distinguishes them)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(100)        NOT NULL,
            email       VARCHAR(150) UNIQUE NOT NULL,
            password    VARCHAR(255)        NOT NULL,
            role        ENUM('buyer','seller') NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Products table (only sellers add products)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            seller_id   INT            NOT NULL,
            name        VARCHAR(200)   NOT NULL,
            description TEXT,
            price       DECIMAL(10,2)  NOT NULL,
            stock       INT DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users(id)
        )
    """)

    # ── Orders table (buyer places an order for a product)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            buyer_id    INT           NOT NULL,
            product_id  INT           NOT NULL,
            quantity    INT           NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status      ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
            ordered_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (buyer_id)   REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # ── Cart table (temporary items before placing an order)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            buyer_id    INT NOT NULL,
            product_id  INT NOT NULL,
            quantity    INT NOT NULL DEFAULT 1,
            FOREIGN KEY (buyer_id)   REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database and tables ready.")
