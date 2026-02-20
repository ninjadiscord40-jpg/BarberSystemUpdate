import sqlite3

def reset_after_shift():

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("DELETE FROM orders")
    cur.execute("DELETE FROM order_items")

    con.commit()
    con.close()
