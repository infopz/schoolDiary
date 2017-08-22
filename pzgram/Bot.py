import requests
import time
import traceback
from multiprocessing import Process, Manager

from .ExceptionFile import *
from .Bot_Class import *
from .api_file import api_request


class Bot:

    def __init__(self, key):
        self.botKey = key
        self.offset = 0
        self.started = False
        self.commands = {}
        self.useful_function = {}
        self.timers = {}
        self.allow_edited_message = False
        self.accept_old_message = False
        # setting bool for funcion
        self.start_action = False  # cambiare, maybe con un dict
        self.help_command = False
        self.start_command = False
        self.before_division = False
        self.after_division = False
        self.default_keyboard = None
        print("Bot Created")

    def set_commands(self, command_dict):
        self.commands = {}
        for i in command_dict:
            self.commands[i] = Command(i, command_dict[i])
        if '/start' in self.commands:
            self.start_command = True
        if '/help' in self.commands:
            self.help_command = True

    def set_function(self, function_dict):
        self.useful_function = {}
        for i in function_dict:
            self.useful_function[i] = Function(function_dict[i])
        if 'start_action' in self.useful_function:
            self.start_action = True
        if 'before_division' in self.useful_function:
            self.before_division = True
        if 'after_division' in self.useful_function:
            self.after_division = True

    def set_timers(self, timer_dict):
        self.timers = timer_dict

    def download_file(self, file_path, local_path=''):
        url = f'https://api.telegram.org/file/bot{self.botKey}/{file_path}'
        local_filename = url.split('/')[-1]
        try:
            r = requests.get(url, stream=True)
            with open(local_path+local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            raise RequestError(str(e))

    def get_updates(self):
        p = {'offset': self.offset, 'limit': 5, 'timeout': 1000}
        while True:
            update = api_request(self.botKey, 'getUpdates', p)
            if update == 'apiError':
                continue
            if not update['ok']:
                print('Error with the update, continue')
                print(update['description'])
                continue
            if len(update['result']) != 0:
                data = update['result']
                self.offset = data[-1]['update_id'] + 1
                return data
            else:
                time.sleep(0.5)

    def run(self):
        shared = Manager().dict()
        process = []
        p1 = Process(target=self.run_bot, args=(shared,))
        process.append(p1)
        if len(self.timers) != 0:
            p2 = Process(target=self.run_timer, args=(shared,))
            process.append(p2)
        self.start_bot(shared)
        for p in process:
            p.start()
        try:
            for p in process:
                p.join()
        except KeyboardInterrupt:  # FIXME: study betterd
            print("Shutting Down...")
            for p in process:
                p.terminate()

    def run_bot(self, shared):
        try:
            print('Bot Started')
            self.started = True
            while True:
                updates = self.get_updates()
                for u in updates:
                    try:
                        message = self.parse_update(u)
                        if message.date < self.start_date and not self.accept_old_message:
                            continue
                        if message.edited and not self.allow_edited_message:
                            continue
                        chat = message.chat
                        arguments = []
                        if message.type == 'command':
                            arguments = message.text.split()[1:]
                        if self.before_division:
                            args = create_parameters_tuple(self.useful_function['before_division'].param,
                                                           self, chat, message, arguments, shared)
                            self.useful_function['before_division'].func(*args)
                        if message.type == 'command':
                            self.divide_command(message, chat, shared)
                            continue  # Step Over the after_division
                        if self.after_division:
                            args = create_parameters_tuple(self.useful_function['after_division'].param,
                                                           self, chat, message, arguments, shared)
                            self.useful_function['after_division'].func(*args)
                    except Exception as e:
                        if str(e) == 'KeyboardInterrupt':
                            pass
                        else:
                            traceback.print_exc()
        except KeyboardInterrupt:
            pass

    def start_bot(self, shared):
        api_request(self.botKey, 'getMe')  # Check Api and Conncction
        self.start_date = datetime.now()
        if self.start_action:
            arg = []
            for i in self.useful_function['start_action'].param:
                if i == 'bot':
                    arg.append(self)
                elif i == 'shared':
                    arg.append(shared)
            self.useful_function['start_action'].func(*tuple(arg))

    def run_timer(self, shared):
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
            parameters = inspect.getfullargspec(func).args
            while True:
                arg = []
                for j in parameters:
                    if j == 'bot':
                        arg.append(self)
                    elif j == 'shared':
                        arg.append(shared)
                func(*tuple(arg))
                time.sleep(delay)
        except KeyboardInterrupt:
            pass

    def parse_update(self, update):
        message = parse_message(update['message'], self)
        return message

    def divide_command(self, message, chat, shared):
        text_split = message.text.split()
        command_name = text_split[0]
        if '@' in text_split[0]:  # if /command@botName
            command_name = text_split[0].split('@')[0]
        if command_name == '/start' or command_name == '/help':
            if command_name == '/start' and not self.start_command:
                default_start(chat, message, self.commands)
                return
            if command_name == '/help' and not self.help_command:
                default_help(chat, self.commands)
                return
        try:
            parameters = self.commands[command_name].param
        except KeyError:
            command_not_found(chat, command_name)
            return
        arguments = text_split[1:]
        args = create_parameters_tuple(parameters, self, chat, message, arguments, shared)
        self.commands[command_name].func(*args)

    def set_keyboard(self, buttons, resize=True):
        self.default_keyboard = create_keyboard(buttons, res=resize)
