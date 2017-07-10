from datetime import datetime

import pzgram.ExceptionFile as ExceptionFile


class Diary:

    def __init__(self):
        self.days = {}
        self.subjects = []

    def add_test(self, date, subject, arg, notes=""):
        newtest = Test(date, subject, arg, notes)
        if date in self.days.keys():
            self.days[date].append(newtest)
        else:
            self.days[date] = [newtest]

    def view_all(self):
        s = ''
        for i in self.days:
            for j in self.days[i]:
                s += str(j)
        return s

    def __str__(self):
        return str(len(self.days))


class Test:

    def __init__(self, date, subject, arguments, notes=""):
        self.subject = subject
        self.date = date
        self.arg = arguments
        self.notes = notes

    def __str__(self):
        return self.date.strftime("%d/%m") + ' ' + self.subject.capitalize() + ' test\n'
        # FIXME: To change when I create the subject class


class Subject:

    def __init__(self, name, abbreviation=""):
        self.name = name
        if abbreviation == "":
            abbreviation = name[0:3]
        self.short = abbreviation
        self.emoji = ''
        self.grades = []

    def __str__(self):
        s = ""
        for i in self.grades:
            s += i.date.strftime("%d/%m") + ' ' + str(i.number) + '\n'
        return s


class Grade:

    def __init__(self, grade, date, type="written"):  # Type: Written, Oral, Practical
        self.numero = grade
        self.date = date
        self.type = type


class Homework:

    def __init__(self, date, subject, notes):
        self.date = date
        self.subject = subject
        self.note = notes
        self.finished = False

    def modify_status(self):
        self.finished = not self.finished


def create_date(day, month):
    try:
        month = int(month)
        year = 2018
        if month >= 7:  # check for changing year
            year = 2017
        year = str(year)
        month = str(month)
        if len(month) == 1:  # trasform 5 in 05
            month = "0"+month
        day = str(day)
        if len(day) == 1:
            day = "0"+day
        return datetime.strptime(day+month+year, "%d%m%Y")
    except Exception as e:
        raise ExceptionFile.DataCreationError()
