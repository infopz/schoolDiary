from datetime import datetime
import inspect

message_possible_type = ['text', 'audio', 'document', 'game', 'photo', 'sticker', 'video', 'voice', 'video_note',
                         'contact', 'location', 'venue']


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


class Function:

    def __init__(self, func):
        self.func = func
        self.param = inspect.getfullargspec(func).args
        self.exec = ''

    def create_execution_string(self, bot, chat, message, shared, args):
        pass

    def call_f(self):
        exec(self.exec)


class Chat:

    def __init__(self, id, bot, **kwargs):
        self.id = id
        self.bot = bot
        for k, v in kwargs.items():
            exec('self.'+k + '=v')

    def send(self, text, parse_mode="Markdown", disable_preview=False, disable_notification=False,
             reply=None, reply_markup=None):
        parameter = {
            'text': text,
            'chat_id': self.id,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply,
            'reply_markup': reply_markup
        }
        self.bot.api_request('sendMessage', parameter)


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

    def reply(self, text):
        self.chat.send(text, reply=self.id)


class User:

    def __init__(self, id, first_name, **kwargs):
        self.id = id
        self.first_name = first_name
        for k, v in kwargs.items():
            exec('self.'+k + '=v')


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
                 'reply_to_message', 'edit_date', 'caption']  # FIXME: put caption in photo/video class
    to_pass = {}
    for i in parameter:
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
            to_pass[i] = message_dict[i]
            break
            # TODO: manage other type
    if 'edit_date' in to_pass:
        return Message(id, chat, date, True, **to_pass)
    return Message(id, chat, date, False, **to_pass)


