import sqlite3
from config import DB_PATH
from config import ADMIN_IDS

# Установление соединения с базой данных
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблиц
def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        role TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS registration_requests (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        unit TEXT,
        stock INTEGER
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    
    # Добавляем администраторов в таблицу users
    for admin_id in ADMIN_IDS:
        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (admin_id,))
        admin = cursor.fetchone()
        if not admin:
            cursor.execute("INSERT INTO users (telegram_id, role) VALUES (?, ?)", (admin_id, 'admin'))
            conn.commit()
    
    conn.commit()
