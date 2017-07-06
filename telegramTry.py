import requests
import time
import json
import main
import inspect

import apiKey

class Bot:

    def __init__(self, key):
        self.botKey = key
        self.offset = 0
        self.commanddict = {}
        print("bot created")

    def api_request(self, method, p={}):
        try:
            data = requests.get(f"https://api.telegram.org/bot{self.botKey}/{method}", params=p)
        except Exception as e:
            print('Request error - '+str(e))
            return {}  # FIXME usare delle eccezioni
        if data.status_code == 200:  # 409 -> Other istance
            data = data.json()
            return data
        else:
            return {}  # FIXME stessa cosa

    def get_update(self):
        p = {'offset': self.offset, 'limit': 1, 'timeout': 1800}
        while True:
            update = self.api_request('getUpdates', p)
            if not update['ok']:
                print('Error with the update, countinue')
                continue
            if len(update['result']) != 0:
                data = update['result'][0]
                self.offset = data['update_id'] + 1
                return data
            else:
                time.sleep(0.5)

    def run(self):
        while True:
            update = self.get_update()
            chat = Chat(update['message']['chat'], self)
            i = inspect.getfullargspec(self.commanddict[update['message']['text']]).args
            arg = []
            for j in i:
                if j == 'chat':
                    arg.append(chat)
                if j == 'bot':
                    arg.append(self)
            args = tuple(arg)
            self.commanddict[update['message']['text']](*args)



class Chat:

    def __init__(self, chat_dict, bot):
        self.dict = chat_dict  # da mettere a posto
        self.bot = bot

    def send(self, text):
        parameter = {
            'text': text,
            'chat_id': self.dict['id']
        }
        self.bot.api_request('sendMessage', parameter)


bot = Bot(apiKey.apiBot)
bot.commanddict = {'/try': main.tryFunc, '/try2': main.secondFunct}
bot.run()