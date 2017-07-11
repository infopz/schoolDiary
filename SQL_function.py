import sqlite3


def create_tables():
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE Test (Subject TEXT, Date TEXT, Arguments TEXT, Notes TEXT)")
        cur.execute("CREATE TABLE Homework (Subject TEXT, Date TEXT, Notes TEXT, Finished INT)")


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
        cur.execute(f"INSERT INTO Homework VALUES ('{subj}', {date}, '{notes}', 0)")


def find_commitments(date):
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT Subject, Arguments, Notes FROM Test WHERE Date = '{date}'")
        test = cur.fetchall()
        cur.execute(f"SELECT Subject, Notes, Finished FROM Homework WHERE Date = '{date}'")
        homework = cur.fetchall()
    return test, homework


def find_all():
    con = sqlite3.connect('diary.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Test")
        test = cur.fetchall()
        cur.execute("SELECT * FROM Homework")
        homework = cur.fetchall()
    return test, homework
