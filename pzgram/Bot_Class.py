from datetime import datetime
import inspect
import json

from .api_file import api_request

message_possible_type = ['text', 'audio', 'document', 'game', 'photo', 'sticker', 'video', 'voice', 'video_note',
                         'contact', 'location', 'venue']
message_all_attributes = ['text', 'audio', 'document', 'game', 'photo', 'sticker', 'video', 'voice', 'video_note',
                          'contact', 'location', 'venue', 'sender', 'forward_from', 'forward_from_chat',
                          'forward_from_message_id', 'forward_date', 'reply_to_message', 'edit_date']
chat_all_attributes = ['title', 'username', 'first_name', 'last_name', 'photo']
user_all_attributes = ['last_name', 'username', 'language_code']


class Command:

    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.param = inspect.getfullargspec(func).args
        self.args = None

    def create_arg(self, bot, chat, message, shared, arguments):
        arg = []
        for j in self.param:
            if j == 'chat':
                arg.append(chat)
            elif j == 'bot':
                arg.append(bot)
            elif j == 'message':
                arg.append(message)
            elif j == 'args':
                arg.append(arguments)
            elif j == 'shared':
                arg.append(shared)
        self.args = tuple(arg)

    def call_f(self):
        self.func(self.args)


class Function:  # FIXME: check

    def __init__(self, func):
        self.func = func
        self.param = inspect.getfullargspec(func).args


class Chat:

    def __init__(self, id, bot, **kwargs):
        self.id = id
        self.bot = bot
        for k, v in kwargs.items():
            exec('self.'+k + '=v')
        for i in chat_all_attributes:
            if not hasattr(self, i):
                exec('self.'+i+'=None')

    def send(self, text, parse_mode="Markdown", disable_preview=False, disable_notification=False,
             reply=None, reply_markup=None, no_keyboard=False):
        if no_keyboard:
            reply_markup = json.dumps({'remove_keyboard': True})
        if reply_markup is None:
            reply_markup = self.bot.default_keyboard
        parameter = {
            'text': text,
            'chat_id': self.id,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply,
            'reply_markup': reply_markup
        }
        api_request(self.bot.botKey, 'sendMessage', parameter)


class Message:

    def __init__(self, id, chat, date, edited, **kwargs):
        self.id = id
        self.chat = chat
        self.date = date
        self.edited = edited
        for k, v in kwargs.items():
            exec('self.'+k + '=v')
        for i in message_possible_type:  # set the type of this message
            if i in kwargs:
                self.type = i
        if self.type == 'text' and self.text.startswith('/'):
            self.type = 'command'
        for i in message_all_attributes:
            if not hasattr(self, i):
                exec('self.'+i+'=None')

    def reply(self, text):  # FIXME, add all the options for chat.send
        self.chat.send(text, reply=self.id)


class User:

    def __init__(self, id, first_name, **kwargs):
        self.id = id
        self.first_name = first_name
        for k, v in kwargs.items():
            exec('self.'+k + '=v')
        for i in user_all_attributes:
            if not hasattr(self, i):
                exec('self.'+i+'=None')


class Photo:

    def __init__(self, bot, id, width, height, file_size=None, other_size=None, caption=None):
        self.bot = bot
        self.file_id = id
        self.width = width
        self.height = height
        self.file_size = file_size
        self.other_size = other_size
        self.text = caption

    def save(self, path=''):
        try:
            get_file = api_request(self.bot.botKey, 'getFile', {'file_id': self.file_id})
            if get_file == 'apiError' or not get_file['ok']:
                return ''
            self.bot.download_file(get_file['result']['file_path'], path)
            return local_filename
        except:
            return ''


def command_not_found(chat, command):
    m = f'Command *{command}* not found\nUse /help for the list of possible commads'
    chat.send(m)


def parse_chat(chat_dict, bot):
    chat_id = chat_dict.pop('id')
    return Chat(chat_id, bot, **chat_dict)


def parse_user(user_dict):
    user_id = user_dict.pop('id')
    user_first_name = user_dict.pop('first_name')
    return User(user_id, user_first_name, **user_dict)


def parse_message(message_dict, bot):
    chat = parse_chat(message_dict['chat'], bot)
    date = datetime.fromtimestamp(int(message_dict['date']))
    id = message_dict['message_id']
    parameter = ['from', 'forward_from', 'forward_from_chat', 'forward_from_message_id', 'forward_date',
                 'reply_to_message', 'edit_date']
    to_pass = {}
    for i in parameter:  # check all possible types, parse what found and add them to to_pass dict
        if i in message_dict:
            if i == parameter[3]:
                to_pass[i] = message_dict[i]
            elif i == parameter[4] or i == parameter[6]:
                date_f = datetime.fromtimestamp(int(message_dict[i]))
                to_pass[i] = date_f
            elif i == parameter[0]:
                u = parse_user(message_dict[i])
                to_pass['sender'] = u
            elif i == parameter[1]:
                u = parse_user(message_dict[i])
                to_pass[i] = u
            elif i == parameter[2]:
                c = parse_chat(message_dict[i], bot)
                to_pass[i] = c
            elif i == parameter[5]:
                m = parse_message(message_dict[i], bot)
                to_pass[i] = m
    for i in message_possible_type:
        if i in message_dict:
            if i == 'text':
                to_pass[i] = message_dict[i]
            elif i == 'photo':
                text = None
                if 'caption' in message_dict:
                    text = message_dict['caption']
                aviable_size = []
                for p in message_dict['photo']:
                    if 'file_size' in p:
                        aviable_size.append(Photo(bot, p['file_id'], p['width'], p['height'], p['file_size'], text))
                    else:
                        aviable_size.append(Photo(bot, p['file_id'], p['width'], p['height'], caption=text))
                biggest_photo = aviable_size[-1]
                del aviable_size[-1]
                biggest_photo.other_size = aviable_size
                to_pass[i] = biggest_photo
            # TODO: manage other type
    if 'edit_date' in to_pass:
        return Message(id, chat, date, True, **to_pass)
    return Message(id, chat, date, False, **to_pass)


def create_parameters_tuple(parameters, bot, chat, message, shared, arguments=[]):
    arg = []
    for j in parameters:
        if j == 'chat':
            arg.append(chat)
        elif j == 'bot':
            arg.append(bot)
        elif j == 'message':
            arg.append(message)
        elif j == 'args':
            arg.append(arguments)
        elif j == 'shared':
            arg.append(shared)
    return tuple(arg)


def create_keyboard(button, one=False, res=True):
    keyb = {"keyboard": button, "one_time_keyboard": one, "resize_keyboard": res}
    keyb = json.dumps(keyb)
    return keyb


def default_start(chat, message, commands):
    possible_commands = ''
    for c in commands:
        possible_commands += commands[c].name + '\n'
    chat.send('Hi, '+message.sender.first_name+"\nhere's the list of possible commands:\n"+possible_commands)


def default_help(chat, commands):
    possible_commands = ''
    for c in commands:
        possible_commands += commands[c].name + '\n'
    chat.send("Here's the list of possible commands:\n" + possible_commands)

def calc_delay(delay):
    seconds_today = (datetime.now().hour * 3600) + (datetime.now().minute * 60) + datetime.now().second
    rem = seconds_today % delay
    new_delay = delay - rem
    return new_delay
