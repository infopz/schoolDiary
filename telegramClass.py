class Chat:

    def __init__(self, chat_dict, bot):
        self.dict = chat_dict  # da mettere a posto
        self.bot = bot

    def send(self, text, parse_mode="Markdown", disable_preview=False, disable_notification=False,
             reply=None, reply_markup=None):
        parameter = {
            'text': text,
            'chat_id': self.dict['id'],
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply,
            'reply_markup': reply_markup
        }
        self.bot.api_request('sendMessage', parameter)


class Message:

    def __init__(self, id, chat, date, text="", sender=''):
        self.id = id
        self.chat = chat
        self.text = text
        self.date = date
        self.sender = sender

    def reply(self, text):
        self.chat.send(text, reply=self.id)


class User:

    def __init__(self, id=None, first_name="", last_name="", username=""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


def command_not_found(chat, command):
    m = f'Command *{command}* not found\nUse /help for the list of possible commads'
    chat.send(m)
