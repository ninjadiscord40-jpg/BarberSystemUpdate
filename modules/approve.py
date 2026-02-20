import sqlite3

def check_admin_password(password):

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("SELECT username FROM accounts WHERE password=? AND role='admin'", (password,))

    result = cur.fetchone()

    con.close()

    return result
