import telegram

def new_verifica(message):
    pass

def start_action(): #setting funciotn
    print("Bot Started")


def timers(): #funcion for all timers
    pass


def message_received(chat, message, user): #main function
    pass

off = 0
print("Initializing Bot")
while True:
    d = telegram.getDataAndTimer(off)
    try:
        if off == 0:
            start_action()
        if d.__class__.__name__ == "List":
            off = d['update_id'] + 1
            user = d['message']['from']
            message = {
                'message_id': d['message']['message_id'],
                'text': d['message']['text'],
                'date': d['message']['date']}
            chat = d['message']['chat']
            message_received(chat, message, user)
        else:
            if d == 'time':
                timers()
    except Exception as e:
        # telegram.sendMess('Errore Interno\n'+str(e), 20403805)
        print('Errore Interno - '+str(e))
