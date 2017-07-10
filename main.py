import pzgram
import pickle

from classFile import *
import apiKey


bot = pzgram.Bot(apiKey.apiBot)


def new_test(message, chat, shared, args):  # now /newverifica nDay nMonth subject other
    d = shared['diary']
    data = create_data(args[0], args[1])
    d.add_test(data, args[2], args[3])  # FIXME: find subject + other arguments
    chat.send("Test added to your diary")
    shared['diary'] = d


def view_calendar(chat, shared):
    d = shared['diary']
    chat.send("Here's yours commitments:\n"+d.view_all())


def save_data(shared):
    diary = shared['diary']
    f = open('diary.txt', 'wb')
    pickle.dump(diary, f)
    f.close()


def load_data(shared):
    f = open('diary.txt', 'rb')
    diary = pickle.load(f)
    shared['diary'] = diary


def start_action(shared):  # setting function
    shared['diary'] = Diary()


def timers():  # funcion for all timers
    pass


bot.set_commands({'/newtest': new_test, '/calendar': view_calendar})
bot.set_function({'start_action': start_action})
bot.run()
