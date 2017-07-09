import time
from classFile import *

import apiKey
import pzgram


bot = pzgram.Bot(apiKey.apiBot)


def new_verifica(message, chat, shared, args):  # per ora /newverifica nGiorno nMese materia other
    d = shared['diario']
    data = create_data(args[0], args[1])
    d.add_verifica(data, args[2], args[3])  # FIXME: trovare materia + altri argomenti
    chat.send("Verifica aggiunta al diario")
    print(d)
    shared['diario'] = d


def viewcalendar(chat, shared):
    d = shared['diario']
    print(d)
    chat.send("Ecco gli impegni in programma:\n"+d.view_all())


def start_action(shared):  # setting function
    shared['diario'] = Diario()


def timers():  # funcion for all timers
    '''day = str(int(time.strftime("%d%m")) - 1)  # FIXME: e' un obrobrio e gestire cambio mese/anno
    try:
        verifiche = diario[day]
    except IndexError:
        return
    if time.strftime('%H') == '14':
        s = "Ehi, domani hai queste"'''


bot.set_commands({'/newverifica': new_verifica, '/calendar': viewcalendar})
bot.set_function({'start_action': start_action})
bot.run()
