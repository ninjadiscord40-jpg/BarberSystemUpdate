import sqlite3
from datetime import datetime
from log_system import add_log

def save_order(order_number, items, total, barber, discount, approved_by, user):

    try:
        con = sqlite3.connect("data.db", timeout=10)
        cur = con.cursor()

        # حفظ الأوردر
        cur.execute("""
            INSERT INTO orders(order_number,total,barber,discount,approved_by,date)
            VALUES(?,?,?,?,?,?)
        """, (order_number, total, barber, discount, approved_by, datetime.now().date()))

        order_id = cur.lastrowid

        # حفظ عناصر الأوردر
        for i in items:
            cur.execute("""
                INSERT INTO order_items(order_id,service_name,price)
                VALUES(?,?,?)
            """, (order_id, i[0], i[1]))

        con.commit()

        add_log("تنفيذ أوردر", f"رقم الأوردر {order_number}", user)

    except Exception as e:
        print("Error saving order:", e)

    finally:
        con.close()
