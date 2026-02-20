import sqlite3

def get_barbers():

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("SELECT name FROM barbers")

    data = [b[0] for b in cur.fetchall()]

    con.close()

    return data
