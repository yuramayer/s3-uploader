"""Adding new admin to the db manually"""

import os
import logging
import sqlite3
import bcrypt


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'users.db')

logger = logging.getLogger(__name__)


def add_user():
    """Func for the manual adding the admins to the db"""
    username = input("Введите логин нового пользователя: ").strip()
    password = input("Введите пароль: ").strip()

    if not username or not password:
        logger.info("❌ Логин и пароль не могут быть пустыми.")
        return

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (username, password_hash) \
                    VALUES (?, ?)',
                    (username, password_hash))
        conn.commit()
        logger.info("✅ Пользователь %s успешно добавлен", username)
    except sqlite3.IntegrityError:
        logger.info("❌ Такой пользователь уже существует")
    finally:
        conn.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    )
    add_user()
