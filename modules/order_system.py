import sqlite3

def get_next_order_number():

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("SELECT order_number FROM orders ORDER BY id DESC LIMIT 1")
    last = cur.fetchone()

    con.close()

    if last:
        num = int(last[0]) + 1
    else:
        num = 1

    return f"{num:03d}"
