import sqlite3
from datetime import datetime

def add_log(action, note, user):

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("INSERT INTO logs(action,note,user,date) VALUES(?,?,?,?)",
                (action, note, user, datetime.now()))

    con.commit()
    con.close()
