import pzgram
import pickle
import json

from classFile import *
import apiKey
import useful_function


bot = pzgram.Bot(apiKey.apiBot)


def new_test_1(chat, shared):  # select month
    shared['data_cache'] = {}  # reset cache
    keyboard = pzgram.create_keyboard([['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'],
                                       ['Sep', 'Oct', 'Nov', 'Dec']], one=True)  # FIXME: give priority to current month
    chat.send('Select a month:', reply_markup=keyboard)
    shared['status'] = 'newTest1'


def new_test_2(message, chat, shared):  # select day
    days = [[], [], [], [], [], [], []]
    for i in range(1, 32):  # FIXME: check int
        days[(i-1)//5].append(str(i))
    month = useful_function.convert_month(message.text)
    if month != '':
        cache = shared['data_cache']
        cache['month'] = month
        cache['day_keyb'] = days
        shared['data_cache'] = cache
    else:
        chat.send('The month that you gave me is not correct')
        new_test_1(chat, shared)
        return
    keyboard = pzgram.create_keyboard(days, one=True)  # FIXME: same thing as month
    chat.send('Now Select a day:', reply_markup=keyboard)
    shared['status'] = 'newTest2'


def new_test_3(message, chat, shared):  # select subject
    cache = shared['data_cache']
    diary = shared['diary']
    day = message.text
    if int(day) in range(1, 32):  # manage with try
        cache['day'] = day
    else:
        chat.send('The day that you gave me is not correct')
        chat.send('Now Select a day:', reply_markup=cache['day_keyb'])
        shared['status'] = 'newTest2'
        return
    try:
        date = create_date(day, cache['month'])
    except pzgram.DataCreationError:
        chat.send('Error while creating the date, retry')
        new_test_1(chat, shared)
        return
    cache['date'] = date
    subj = [[], [], []]
    for i in range(len(diary.subjects)):
        subj[i//3].append(diary.subjects[i].short)
    keyboard = pzgram.create_keyboard(subj, one=False)
    chat.send("Nice, now select the subject:", reply_markup=keyboard)
    shared['status'] = 'newTest3'
    cache['subj_keyb'] = keyboard
    shared['data_cache'] = cache


def new_test_4(message, chat, shared):
    cache = shared['data_cache']
    diary = shared['diary']
    for i in range(len(diary.subjects)):
        if diary.subjects[i].short == message.text:
            cache['subject'] = diary.subjects[i].name
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Nice, now select the subject:", reply_markup=cache['subj_keyb'])
    chat.send('Ok, last step, send me the arguments of this test:', reply_markup=json.dumps({'remove_keyboard': True}))
    shared['status'] = 'newTest4'
    shared['data_cache'] = cache


def new_test_5(message, chat, shared):
    diary = shared['diary']
    cache = shared['data_cache']
    text = message.text.split('\n', 1)
    if len(text) == 2:
        diary.add_test(cache['date'], cache['subject'], text[0], text[1])
    else:
        diary.add_test(cache['date'], cache['subject'], text[0])
    chat.send("Test added to your diary")
    shared['data_cache'] = {}
    shared['status'] = ''
    shared['diary'] = diary


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


def create_subject(shared):
    diary = shared['diary']
    subject_list = {'Math': 'Math', 'Italian': 'Ita', 'English': 'Eng', 'Sistemi': 'Sis', 'TPS':'TPS',
                    'History': 'Hist', 'Gymnastic': 'Gym', 'Telecommunications': 'Tele'}
    for m in subject_list:
        diary.subjects.append(Subject(m, subject_list[m]))
    shared['diary'] = diary


def process_message(message, chat, shared):
    if shared['status'] == 'newTest1':
        new_test_2(message, chat, shared)
    elif shared['status'] == 'newTest2':
        new_test_3(message, chat, shared)
    elif shared['status'] == 'newTest3':
        new_test_4(message, chat, shared)
    elif shared['status'] == 'newTest4':
        new_test_5(message, chat, shared)


def start_action(shared):
    shared['diary'] = Diary()
    shared['status'] = ''
    shared['data_cache'] = {}
    create_subject(shared)


bot.set_commands({'/newtest': new_test_1, '/calendar': view_calendar})
bot.set_function({'start_action': start_action, 'after_division': process_message})
bot.run()
