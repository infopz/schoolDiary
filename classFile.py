from datetime import datetime

import pzgram.ExceptionFile


class Diario:

    def __init__(self):
        self.giorni = {}
        self.materie = {}

    def add_verifica(self, data, materia, arg):  # per ora /newverifica nGiorno nMese materia other
        newverifica = Verifica(data, materia, arg)
        if data in self.giorni.keys():
            self.giorni[data].append(newverifica)
        else:
            self.giorni[data] = [newverifica]
        print(len(self.giorni))

    def view_all(self):
        s = ''
        for i in self.giorni:
            for j in self.giorni[i]:
                s += str(j)
        return s

    def __str__(self):
        return str(len(self.giorni))


class Verifica:

    def __init__(self, data, materia, argomenti, note=""):
        self.materia = materia
        self.data = data
        self.arg = argomenti
        self.note = note

    def __str__(self):
        return self.data.strftime("%d/%m") + ' Verifica di ' + self.materia + '\n'  #  FIXME: da cambiare quando faccio materia


class Materia:

    def __init__(self, nome, abbreviazione=""):
        self.nome = nome
        if abbreviazione == "":
            abbreviazione = nome[0:3]
        self.short = abbreviazione
        self.voti = []

    def __str__(self):
        s = ""
        for i in self.voti:
            s += i.data.strftime("%d/%m") + ' ' + str(i.numero) + '\n'
        return s


class Voto:

    def __init__(self, voto, data, tipo="Scritto"):  # Tipo: Scritto, Orale o Pratico
        self.numero = voto
        self.data = data
        self.tipo = tipo


class Compito:

    def __init__(self, data, materia, note):
        self.data = data
        self.materia = materia
        self.note = note
        self.completato = False

    def modify_status(self):
        self.completato = not self.completato


def create_data(day, month):
    try:
        month = int(month)
        year = 2018
        if month >= 7:  #check per cambio anno
            year -= 1
        year = str(year)
        month = str(month)
        if len(month) == 1:
            month = "0"+month
        day = str(day)
        if len(day) == 1:
            day = "0"+day
        return datetime.strptime(day+month+year, "%d%m%Y")
    except Exception as e:
        raise ExceptionFile.DataCreationError()
