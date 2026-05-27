"""
models/user.py
──────────────
User model — wraps all DB operations related to users.
Demonstrates OOP: class with methods that talk to MySQL.
"""

import hashlib
from db.connection import get_connection


def _hash(password: str) -> str:
    """SHA-256 hash — never store plain-text passwords."""
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(self, id, name, email, role):
        self.id    = id
        self.name  = name
        self.email = email
        self.role  = role          # 'buyer' or 'seller'

    # ── Class method: register a new user ───────────────────────────────────
    @classmethod
    def register(cls, name, email, password, role):
        """
        Insert a new user row.
        Returns the new User object, or raises ValueError if email exists.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
                (name, email, _hash(password), role)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return cls(new_id, name, email, role)
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError("Email already registered.")
            raise e
        finally:
            cursor.close()
            conn.close()

    # ── Class method: login ──────────────────────────────────────────────────
    @classmethod
    def login(cls, email, password):
        """
        Verify credentials.
        Returns a User object on success, None on failure.
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)    # returns rows as dicts
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, _hash(password))
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return cls(row["id"], row["name"], row["email"], row["role"])
        return None
