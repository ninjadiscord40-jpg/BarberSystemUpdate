import sqlite3


def setup():

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # ===== جدول الحسابات =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # ===== جدول الخدمات =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)

    # ===== جدول الموظفين =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS barbers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # ===== جدول الأوردرات =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT,
        total REAL,
        barber TEXT,
        discount REAL,
        approved_by TEXT,
        created_by TEXT,
        date TEXT
    )
    """)

    # ===== جدول تفاصيل الأوردر =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        service_name TEXT,
        price REAL
    )
    """)

    # ===== جدول الإضافة والإخراج الحالي =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cash_actions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        note TEXT,
        date TEXT
    )
    """)

    # ===== جدول سجل دائم للإضافة والإخراج =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cash_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        note TEXT,
        created_by TEXT,
        approved_by TEXT,
        date TEXT,
        time TEXT,
        datetime TEXT
    )
    """)

    # ===== جدول الشفت =====
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

    # ===== جدول العملاء (Customer System) =====
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        created_at TEXT
    )
    """)

    # ===== إنشاء حساب admin افتراضي =====
    cur.execute("SELECT * FROM accounts")

    if not cur.fetchone():
        cur.execute("""
        INSERT INTO accounts(username,password,role)
        VALUES('admin','admin','admin')
        """)

    con.commit()
    con.close()


# تشغيل تلقائي
setup()