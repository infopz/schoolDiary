import sqlite3


def create_tables():
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE Test (Subject TEXT, Date TEXT, Arguments TEXT, Notes TEXT)")
        cur.execute("CREATE TABLE Homework (Subject TEXT, Date TEXT, Notes TEXT, Finished INT)")
        cur.execute("CREATE TABLE Votes (Vote FLOAT, Date TEXT, Subject TEXT, Type TEXT, Notes TEXT)")


def add_new_test(subj, date, arg, notes=None):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        if notes is None:
            cur.execute(f"INSERT INTO Test(Subject, Date, Arguments) VALUES ('{subj}', '{date}', '{arg}')")
        else:
            cur.execute(f"INSERT INTO Test VALUES ('{subj}', '{date}', '{arg}', '{notes}')")


def add_new_homework(subj, date, notes):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO Homework VALUES ('{subj}', '{date}', '{notes}', 0)")


def add_new_vote(num, subj, typ, date, notes=None):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        if notes is None:
            cur.execute(f"INSERT INTO Votes(Vote, Subject, Type, Date) VALUES ('{num}', '{subj}', '{typ}', '{date}')")
        else:
            cur.execute(f"INSERT INTO Votes VALUES ('{num}', '{subj}', '{date}', '{notes}')")


def find_one_day(date):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT ROWID, Subject, Arguments, Notes FROM Test WHERE Date = '{date}'")
        test = cur.fetchall()
        cur.execute(f"SELECT ROWID, Subject, Notes, Finished FROM Homework WHERE Date = '{date}'")
        homework = cur.fetchall()
    return test, homework


def find_between(start, stop):  # FIXME: manage the chainging of years
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT ROWID, * FROM Test WHERE Date BETWEEN '{start}' AND '{stop}'")
        test = cur.fetchall()
        cur.execute(f"SELECT ROWID, * FROM Homework WHERE Date BETWEEN '{start}' AND '{stop}'")
        homework = cur.fetchall()
    return test, homework


def get_one_row(table, rowid):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE ROWID = {rowid}")
        row = cur.fetchone()
    return row


def update_value(table, rowid, column, new_value):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        if column == 'Finished':
            cur.execute(f"UPDATE {table} SET {column} = {new_value} WHERE ROWID = {rowid}")
        else:
            cur.execute(f"UPDATE {table} SET {column} = '{new_value}' WHERE ROWID = {rowid}")


def get_vote_date():  # FIXME: manage the changing of years
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Votes ORDER BY Date ASC")
        votes = cur.fetchall()
    return votes


def get_vote_subj(subj):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT Vote, Type, Date, Notes FROM Votes WHERE Subject = '{subj}'")
        rows = cur.fetchall()
    return rows


def get_average(typ):  # True: with Type, False: all votes
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        if typ:
            cur.execute("SELECT AVG(Vote), Subject, Type FROM Votes GROUP BY Subject, Type")
        else:
            cur.execute("SELECT AVG(Vote), Subject FROM Votes GROUP BY Subject")
        avg = cur.fetchall()
    return avg
