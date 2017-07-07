import requests
import time
from datetime import datetime
import json
import main
import inspect
from multiprocessing import Process, Manager

import apiKey
from ExceptionFile import *
from telegramClass import *


class Bot:

    def __init__(self, key):
        self.botKey = key
        self.offset = 0
        self.commands = {}
        self.timers = {}
        self.contol_funcion()
        print("Bot Created")

    def contol_funcion(self):
        try:
            inspect.getfullargspec(main.start_action)
            self.start_action = True
        except AttributeError:
            self.start_action = False
        try:
            inspect.getfullargspec(main.help_command)
            self.help_command = True
        except AttributeError:
            self.help_command = False
        try:
            inspect.getfullargspec(main.start_command)
            self.start_command = True
        except AttributeError:
            self.start_command = False
        try:
            inspect.getfullargspec(main.before_division)
            self.before_division = True
        except AttributeError:
            self.before_division = False
        try:
            inspect.getfullargspec(main.after_division)
            self.after_division = True
        except AttributeError:
            self.after_division = False

    def set_commands(self, command_dict):
        self.commands = command_dict

    def set_timers(self, timer_dict):
        self.timers = timer_dict

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
        p = {'offset': self.offset, 'limit': 1, 'timeout': 1000}
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
        shared = Manager().dict()
        p1 = Process(target=self.seriuosly_run, args=(shared,))
        p2 = Process(target=self.start_timer, args=(shared,))
        p1.start()
        p2.start()
        try:
            p1.join()
            p2.join()
        except KeyboardInterrupt:
            print("Shutting Down....")
            p1.terminate()
            p2.terminate()

    def seriuosly_run(self, shared):
        try:
            if self.start_action:
                main.start_action(shared)  # TODO: same thing
            while True:
                update = self.get_update()
                message = self.parse_update(update)
                chat = message.chat
                if self.before_division:
                    main.before_division()  # TODO: check parameter, also dopo
                text_split = message.text.split()
                if text_split[0].startswith('/'):
                    self.divide_command(text_split, message, chat, shared)
                if self.after_division:
                    main.after_division()
        except KeyboardInterrupt:
            pass

    def start_timer(self, shared):
        timers = []
        for d in self.timers.keys():
            p = Process(target=self.manage_one_timer, args=(d, self.timers[d], shared))
            timers.append(p)
        for p in timers:
            p.start()
        try:
            for p in timers:
                p.join()
        except KeyboardInterrupt:
            for p in timers:
                p.terminate()

    def manage_one_timer(self, delay, func, shared):
        try:
            while True:
                func()
                time.sleep(delay)
        except KeyboardInterrupt:
            pass

    def parse_update(self, update):
        chat = Chat(update['message']['chat'], self)
        sender = User(update['message']['from']['id'], update['message']['from']['first_name'])
        date = datetime.fromtimestamp(int(update['message']['date']))
        message = Message(update['message']['message_id'], chat, date, update['message']['text'], sender)
        return message

    def divide_command(self, text_split, message, chat, shared):
        command_name = ''
        if '@' in text_split[0]:  # if /command@botName
            command_name = text_split[0].split('@')[0]
        else:
            command_name = text_split[0]
        try:
            i = inspect.getfullargspec(self.commands[command_name]).args
        except KeyError:
            command_not_found(chat, command_name)
            return
        arguments = text_split[1:]
        arg = []
        for j in i:
            if j == 'chat':
                arg.append(chat)
            elif j == 'bot':
                arg.append(self)
            elif j == 'message':
                arg.append(message)
            elif j == 'args':
                arg.append(arguments)
            elif j == 'shared':
                arg.append(shared)
        args = tuple(arg)
        self.commands[command_name](*args)
