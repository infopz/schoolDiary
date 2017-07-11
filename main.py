import pzgram
import json
import time

import SQL_function
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
    for i in range(1, 32):
        days[(i-1)//5].append(str(i))
    keyboard = pzgram.create_keyboard(days, one=True)
    month = useful_function.convert_month(message.text)
    if month != '':
        cache = shared['data_cache']
        cache['month'] = month
        cache['day_keyb'] = keyboard
        shared['data_cache'] = cache
    else:
        chat.send('The month that you gave me is not correct')
        new_test_1(chat, shared)
        return
    chat.send('Now Select a day:', reply_markup=keyboard)
    shared['status'] = 'newTest2'


def new_test_3(message, chat, shared):  # select subject
    cache = shared['data_cache']
    subjects = shared['subjects']
    day = message.text
    if int(day) in range(1, 32):  # manage with try
        cache['day'] = day
    else:
        chat.send('The day that you gave me is not correct')
        chat.send('Now Select a day:', reply_markup=cache['day_keyb'])
        shared['status'] = 'newTest2'
        return
    if not useful_function.check_date(day, cache['month']):
        chat.send('Error while creating the date, retry')
        new_test_1(chat, shared)
        return
    cache['date'] = useful_function.create_date(day, cache['month'])
    subj = [[], [], []]
    c = 0
    for i in subjects:
        subj[c//3].append(subjects[i])
        c += 1
    keyboard = pzgram.create_keyboard(subj, one=False)
    chat.send("Nice, now select the subject:", reply_markup=keyboard)
    shared['status'] = 'newTest3'
    cache['subj_keyb'] = keyboard
    shared['data_cache'] = cache


def new_test_4(message, chat, shared):
    cache = shared['data_cache']
    subjects = shared['subjects']
    for i in subjects:
        if subjects[i] == message.text:
            cache['subject'] = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Nice, now select the subject:", reply_markup=cache['subj_keyb'])
    chat.send('Ok, last step, send me the arguments of this test:', reply_markup=json.dumps({'remove_keyboard': True}))
    shared['status'] = 'newTest4'
    shared['data_cache'] = cache


def new_test_5(message, chat, shared):
    cache = shared['data_cache']
    text = message.text.split('\n', 1)
    if len(text) == 2:
        SQL_function.add_new_test(cache['subject'], cache['date'], text[0], text[1])
    else:
        SQL_function.add_new_test(cache['subject'], cache['date'], text[0])
    chat.send("Test added to your diary")
    shared['data_cache'] = {}
    shared['status'] = ''


def new_homework(chat, shared):
    shared['data_cache'] = {}
    keyboard = pzgram.create_keyboard([['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'],
                                       ['Sep', 'Oct', 'Nov', 'Dec']], one=True)
    chat.send('Select a month:', reply_markup=keyboard)
    shared['status'] = 'newHW1'


def new_homework_2(message, chat, shared):
    days = [[], [], [], [], [], [], []]
    for i in range(1, 32):
        days[(i - 1) // 5].append(str(i))
    keyboard = pzgram.create_keyboard(days, one=True)
    month = useful_function.convert_month(message.text)
    if month != '':
        cache = shared['data_cache']
        cache['month'] = month
        cache['day_keyb'] = keyboard
        shared['data_cache'] = cache
    else:
        chat.send('The month that you gave me is not correct')
        new_homework(chat, shared)
        return
    chat.send('Now Select a day:', reply_markup=keyboard)
    shared['status'] = 'newHW2'


def new_homework_3(message, chat, shared):
    cache = shared['data_cache']
    subjects = shared['subjects']
    day = message.text
    if int(day) in range(1, 32):  # manage with try
        cache['day'] = day
    else:
        chat.send('The day that you gave me is not correct')
        chat.send('Now Select a day:', reply_markup=cache['day_keyb'])
        shared['status'] = 'newHW2'
        return
    if not useful_function.check_date(day, cache['month']):
        chat.send('Error while creating the date, retry')
        new_homework(chat, shared)
        return
    cache['date'] = useful_function.create_date(day, cache['month'])
    subj = [[], [], []]
    c = 0
    for i in subjects:
        subj[c // 3].append(subjects[i])
        c += 1
    keyboard = pzgram.create_keyboard(subj, one=False)
    chat.send("Nice, now select the subject:", reply_markup=keyboard)
    shared['status'] = 'newHW3'
    cache['subj_keyb'] = keyboard
    shared['data_cache'] = cache


def new_homework_4(message, chat, shared):
    cache = shared['data_cache']
    subjects = shared['subjects']
    for i in subjects:
        if subjects[i] == message.text:
            cache['subject'] = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Nice, now select the subject:", reply_markup=cache['subj_keyb'])
    chat.send('Ok, last step, send me the notes about this homework:',
              reply_markup=json.dumps({'remove_keyboard': True}))
    shared['status'] = 'newHW4'
    shared['data_cache'] = cache


def new_homework_5(message, chat, shared):
    cache = shared['data_cache']
    SQL_function.add_new_homework(cache['subject'], cache['date'], message.text)
    chat.send("Homework added to your diary")
    shared['data_cache'] = {}
    shared['status'] = ''


def view_calendar(chat, shared):
    s = ''
    tests, homeworks = SQL_function.find_all()
    for t in tests:
        s += useful_function.convert_test(t) + '\n'
    for hw in homeworks:
        s += useful_function.convert_homework(hw) + '\n'
    chat.send("Here's yours commitments:\n"+s)


def allert_timer(bot):
    h = time.strftime('%H')
    print(h)
    if h == '15':
        s = useful_function.check_tomorrow()
        if s != '':
            pzgram.Chat(20403805, bot).send(s)


def process_message(message, chat, shared):
    if shared['status'] == 'newTest1':
        new_test_2(message, chat, shared)
    elif shared['status'] == 'newTest2':
        new_test_3(message, chat, shared)
    elif shared['status'] == 'newTest3':
        new_test_4(message, chat, shared)
    elif shared['status'] == 'newTest4':
        new_test_5(message, chat, shared)
    elif shared['status'] == 'newHW1':
        new_homework_2(message, chat, shared)
    elif shared['status'] == 'newHW2':
        new_homework_3(message, chat, shared)
    elif shared['status'] == 'newHW3':
        new_homework_4(message, chat, shared)
    elif shared['status'] == 'newHW4':
        new_homework_5(message, chat, shared)


def start_action(shared):
    shared['status'] = ''
    shared['data_cache'] = {}
    shared['subjects'] = {'Math': 'Math', 'Italian': 'Ita', 'English': 'Eng', 'Sistemi': 'Sis', 'TPS': 'TPS',
                          'History': 'Hist', 'Gymnastic': 'Gym', 'Telecommunications': 'Tele'}

bot.set_commands({'/newtest': new_test_1, '/calendar': view_calendar, '/newhw': new_homework})  # Change with keyboard
bot.set_function({'start_action': start_action, 'after_division': process_message})
bot.set_timers({7200: allert_timer})
bot.run()
