import requests
import time
from datetime import datetime
import json
import main
import inspect

import apiKey
from ExceptionFile import *


class Bot:

    def __init__(self, key):
        self.botKey = key
        self.offset = 0
        self.commanddict = {}
        print("Bot Created")

    def api_request(self, method, p={}):
        try:
            data = requests.get(f"https://api.telegram.org/bot{self.botKey}/{method}", params=p)
        except Exception as e:
            print('Request error - '+str(e))
            raise RequestError(str(e))
        if data.status_code == 200:  # 409 -> Other istance
            data = data.json()
            return data
        else:
            raise AnotherStatusError(data.status_code)

    def get_update(self):
        p = {'offset': self.offset, 'limit': 1, 'timeout': 1800}
        while True:
            try:
                update = self.api_request('getUpdates', p)
            except AnotherStatusError or RequestError as e:
                if str(e) == '409':
                    print('Another Instance Error, try again')
                time.sleep(3)
                continue
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
            message = self.parse_update(update)
            chat = message.chat
            i = inspect.getfullargspec(self.commanddict[message.text]).args
            arg = []
            for j in i:
                if j == 'chat':
                    arg.append(chat)
                if j == 'bot':
                    arg.append(self)
            args = tuple(arg)
            self.commanddict[message.text](*args)  # TODO: dividere per arg e prendere il primo

    def parse_update(self, update):
        chat = Chat(update['message']['chat'], self)
        sender = User(update['message']['from']['id'], update['message']['from']['first_name'])
        date = datetime.fromtimestamp(int(update['message']['date']))
        message = Message(update['message']['message_id'], chat, date, update['message']['text'], sender)
        return message


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


class Message:

    def __init__(self, id, chat, date, text="", sender=User()):  # TODO: daimo
        self.chat = chat
        self.text = text


class User:

    def __init__(self, id, first_name, last_name="", username=""):  # TODO: daimo
        pass

bot = Bot(apiKey.apiBot)
bot.commanddict = {'/try': main.tryFunc, '/try2': main.secondFunct}
bot.run()