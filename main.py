import time
from classFile import *

import telegram


def new_verifica(message, chat):  # per ora /newverifica nGiorno nMese materia other
    m = message['text'].split()
    data = create_data(m[1], m[2])
    diario.add_verifica(data, m[3], m[4])  # FIXME: trovare materia + altri argomenti
    telegram.sendMess("Verifica aggiunta al diario", chat)


def viewcalendar(chat):
    telegram.sendMess("Ecco gli impegni in programma:\n"+diario.view_all(), chat)


def start_action():  # setting function
    print("Bot Started")


def timers():  # funcion for all timers
    '''day = str(int(time.strftime("%d%m")) - 1)  # FIXME: e' un obrobrio e gestire cambio mese/anno
    try:
        verifiche = diario[day]
    except IndexError:
        return
    if time.strftime('%H') == '14':
        s = "Ehi, domani hai queste"'''


def message_received(chat, message, user): # main function
    if message['text'].startswith('/newverifica'):
        new_verifica(message, chat)
    elif message['text'].startswith('/calendar'):
        viewcalendar(chat)

if __name__ == '__main__':
    off = 0
    diario = Diario()
    print("Initializing Bot")
    while True:
        d = telegram.getDataAndTimer(off)
        try:
            if off == 0:
                start_action()
            if d.__class__.__name__ == "dict":  # FIXME: gestire diversamente la cosa, magari con classi
                off = d['update_id'] + 1
                user = d['message']['from']
                message = {
                    'message_id': d['message']['message_id'],
                    'text': d['message']['text'],
                    'date': d['message']['date']}
                chat = d['message']['chat']
                message_received(chat, message, user)
            else:
                if d == 'time':  # FIXME: cambiare sistema timer, fa schifo, maybe async
                    timers()
        except Exception as e:
            # telegram.sendMess('Errore Interno\n'+str(e), 20403805)
            # print('Errore Interno - '+str(e))
            raise


def tryFunc(chat):
    chat.send("Prova")

def secondFunct(chat, stringa):
    chat.send(stringa)