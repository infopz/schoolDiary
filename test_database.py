import sqlite3 as lite

con = lite.connect('diary.db')
with con:
    #con.row_factory = lite.Row
    cur = con.cursor()
    cur.execute("SELECT AVG(Vote), Subject, Type FROM Votes GROUP BY Subject, Type")
    rows = cur.fetchall()
    print(rows)