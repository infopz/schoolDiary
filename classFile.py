import time

class verifica:

    def __init__(self, data, materia, argomenti, note = ""):
        self.materia = materia
        self.data = data
        self.arg = argomenti
        self.note = note

class materia:

    def __init__(self, nome, tipo = "Scritto", abbreviazione = ""): #Tipo: Scritto, Orale o Pratico
        self.nome = nome
        self.tipo = tipo
        if abbreviazione == "":
            abbreviazione = nome[0:3]
        self.short = abbreviazione
        self.voti = []
        self.media = 0.0

    def __str__(self):
        s = ""
        for i in self.voti:
            

class voto:

    def __init__(self, voto, data):
        self.numero = voto
        self.data = data

class compito:

    pass
