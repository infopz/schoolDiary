import time
from classFile import *

import telegram


def new_verifica(message, chat): # per ora /newverifica nGiorno nMese materia other
    m = message['text'].split()
    data = time.strptime(m[1]+" "+m[2], "%d %m")
    newverifica = verifica(data, m[3], m[4])
    diario[m[1]+m[2]] = [newverifica]
    telegram.sendMess("Verifica aggiunta al diario", chat)


def viewcalendar(chat):
    s = ""
    for i in diario:
        for j in i:
            s += str(j)
    telegram.sendMess("Ecco le verifiche in programma:\n"+s, chat)


def start_action(): # setting function
    print("Bot Started")


def timers(): # funcion for all timers
    day = str(int(time.strftime("%d%m")) - 1) # FIXME: e' un obrobrio e gestire cambio mese/anno
    try:
        verifiche = diario[day]
    except IndexError:
        return
    if time.strftime('%H') == '14':
        s = "Ehi, domani hai queste"


def message_received(chat, message, user): # main function
    if message['text'].startswith('/newverifica'):
        new_verifica(message, chat)
    elif message['text'].startswith('/calendar'):
        viewcalendar(chat)

off = 0
diario = {}
print("Initializing Bot")
while True:
    d = telegram.getDataAndTimer(off)
    try:
        if off == 0:
            start_action()
        if d.__class__.__name__ == "List": # FIXME: gestire diversamente la cosa, magari con classi
            off = d['update_id'] + 1
            user = d['message']['from']
            message = {
                'message_id': d['message']['message_id'],
                'text': d['message']['text'],
                'date': d['message']['date']}
            chat = d['message']['chat']
            message_received(chat, message, user)
        else:
            if d == 'time': # FIXME: cambiare sistema timer, fa schifo, maybe async
                timers()
    except Exception as e:
        # telegram.sendMess('Errore Interno\n'+str(e), 20403805)
        print('Errore Interno - '+str(e))
