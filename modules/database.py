import sqlite3

def create_tables():

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # جدول الحسابات
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # جدول الخدمات
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)

    # جدول الأوردرات
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT,
        total REAL,
        barber TEXT,
        discount REAL,
        approved_by TEXT,
        date TEXT
    )
    """)

    # عناصر الأوردر
    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        service_name TEXT,
        price REAL
    )
    """)

    # الإضافات والإخراج
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cash_actions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        note TEXT,
        date TEXT
    )
    """)

    # جدول الشفت
    cur.execute("""
    CREATE TABLE IF NOT EXISTS shift(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_balance REAL,
        added_money REAL,
        removed_money REAL,
        total_sales REAL,
        received_balance REAL,
        date TEXT
    )
    """)

    # جدول الإعدادات (لترقيم الأوردرات)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # إدخال قيمة ابتدائية لترقيم الأوردرات
    cur.execute("""
    INSERT OR IGNORE INTO settings(key, value)
    VALUES('last_order', '0')
    """)

    con.commit()
    con.close()
