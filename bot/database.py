import sqlite3
from config import DB_PATH
from config import ADMIN_IDS, PRODUCT_TYPES

# Установление соединения с базой данных
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создание таблиц
def init_db():
    # Таблица для пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        role TEXT
    )''')

    # Таблица для заявок на регистрацию
    cursor.execute('''CREATE TABLE IF NOT EXISTS registration_requests (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
    )''')

    # Таблица для типов продуктов
    cursor.execute('''CREATE TABLE IF NOT EXISTS product_types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )''')

    # Таблица для продуктов с внешним ключом на таблицу product_types
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        unit TEXT NOT NULL,
        stock INTEGER DEFAULT 0,
        type_id INTEGER,
        image TEXT,
        FOREIGN KEY(type_id) REFERENCES product_types(id)
    )''')

    # Таблица для заказов
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Инициализация типов продуктов из config.py
    init_product_types()
    # Добавляем администраторов в таблицу users
    init_admins()
    # Сохраняем изменения
    conn.commit()
    
def init_admins():    
    for admin_id in ADMIN_IDS:
        cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (admin_id,))
        admin = cursor.fetchone()
        if not admin:
            cursor.execute("INSERT INTO users (telegram_id, role) VALUES (?, ?)", (admin_id, 'admin'))
            conn.commit()

def init_product_types():
    from config import PRODUCT_TYPES 

    # Добавляем типы в таблицу product_types, если они ещё не добавлены
    for type_name in PRODUCT_TYPES:
        cursor.execute("SELECT id FROM product_types WHERE name = ?", (type_name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO product_types (name) VALUES (?)", (type_name,))
            conn.commit()