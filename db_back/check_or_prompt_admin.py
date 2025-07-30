"""Check & operate on database with admins"""

import os
import logging
import sqlite3
import bcrypt
from config import ADMIN_LOGIN, ADMIN_PASSWORD


logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'users.db')


def ensure_user_table():
    """Creates table 'users' if doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def has_users() -> bool:
    """Checks if there're any users in the admin's database"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM users')
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def prompt_for_admin():
    """Add admin to the database if there's no any users in it"""
    logger.info(
        "\n 🟢 В базе нет пользователей. "
        "Создаём первого администратора"
        )
    username = ADMIN_LOGIN
    password = ADMIN_PASSWORD

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash))
    conn.commit()
    conn.close()
    logger.info("✅ Администратор %s добавлен", username)


def check_or_prompt_admin():
    """Checks if users in the db & adds it"""
    ensure_user_table()
    if not has_users():
        prompt_for_admin()
    else:
        logger.info("✅ Пользователи уже есть в базе")


def get_user_from_db(username: str):
    """Gets user from the db by the login"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT password_hash FROM users WHERE username = ?',
                (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
