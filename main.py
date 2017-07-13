import pzgram
import json
import time

import SQL_function
import apiKey
import useful_function

bot = pzgram.Bot(apiKey.apiBot)


def new_test_1(chat, shared):  # select month
    shared['data_cache'] = {}  # reset cache
    # keyboard = pzgram.create_keyboard([['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'],
    #                                    ['Sep', 'Oct', 'Nov', 'Dec']], one=True)  # FIXME: give priority to current month
    keyboard = pzgram.create_keyboard(useful_function.create_hw_keyboard(), one=True)
    chat.send('Select a month:', reply_markup=keyboard)
    shared['status'] = 'newTest1'


def new_test_2(message, chat, shared):  # select day
    days = [[], [], [], [], [], [], []]
    for i in range(1, 32):
        days[(i-1)//7].append(str(i))
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
    chat.send('Select a date:', reply_markup=shared['keyboards']['days'])
    shared['data_cache'] = {'conv_dict': shared['keyboards']['days_c']}
    shared['status'] = 'newHW1'


def new_homework_2(message, chat, shared):
    cache = shared['data_cache']
    conv_dict = cache['conv_dict']
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                  'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    if message.text in conv_dict:
        cache['date'] = conv_dict[message.text]
        chat.send('Ok, now select a subject:', reply_markup=shared['keyboards']['subj'])
        shared['status'] = 'newHW2'
    elif message.text == 'This Month':
        chat.send('Select a day', reply_markup=shared['keyboards']['this_m'])
        cache['conv_dict'] = shared['keyboards']['this_m_c']
        shared['data_cache'] = cache
    elif message.text == 'Next Month':
        chat.send('Select a day', reply_markup=shared['keyboards']['next_m'])
        cache['conv_dict'] = shared['keyboards']['next_m_c']
        shared['data_cache'] = cache
    elif message.text == 'Other':
        chat.send('Select a month', reply_markup=shared['keyboards']['all_month'])
    elif message.text in month_dict:
        month = month_dict[message.text]
        key_list, conv_dict = useful_function.create_month_keyboard(month)
        keyboard = pzgram.create_keyboard(key_list, one=True)
        chat.send('Now select a day:', reply_markup=keyboard)
        cache['conv_dict'] = conv_dict
    else:
        chat.send('The day that you give me is not correct')
        new_homework(chat, shared)
    shared['data_cache'] = cache


def new_homework_3(message, chat, shared):
    cache = shared['data_cache']
    subjects = shared['subjects']
    for i in subjects:
        if subjects[i] == message.text:
            cache['subject'] = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Nice, now select the subject:", reply_markup=shared['keyboards']['subj'])
    chat.send('Ok, last step, send me the notes about this homework:',
              reply_markup=json.dumps({'remove_keyboard': True}))
    shared['status'] = 'newHW3'
    shared['data_cache'] = cache


def new_homework_4(message, chat, shared):
    cache = shared['data_cache']
    SQL_function.add_new_homework(cache['subject'], cache['date'], message.text)
    chat.send("Homework added to your diary")
    shared['data_cache'] = {}
    shared['status'] = ''


def view_calendar(chat):
    s = ''
    tests, homeworks = SQL_function.find_all()
    for t in tests:
        s += useful_function.convert_test(t) + '\n'
    for hw in homeworks:
        s += useful_function.convert_homework(hw) + '\n'
    chat.send("Here's yours commitments:\n"+s)


def allert_timer(bot):
    h = time.strftime('%H')
    if h == '14':
        s = useful_function.check_tomorrow()
        if s != '':
            pzgram.Chat(20403805, bot).send(s)


def set_keyboard(shared):
    month = int(time.strftime('%m'))
    days_l, days_c = useful_function.create_hw_keyboard()
    this_m_l, this_m_c = useful_function.create_this_month_keyboard()
    next_m_l, next_m_c = useful_function.create_month_keyboard(month+1)
    days = pzgram.create_keyboard(days_l, one=True)
    this_m = pzgram.create_keyboard(this_m_l, one=True)
    next_m = pzgram.create_keyboard(next_m_l, one=True)
    all_month = pzgram.create_keyboard(useful_function.create_all_month_keyboard(), one=True)
    subj = [[], [], []]
    for i, s in enumerate(shared['subjects']):
        subj[i // 3].append(shared['subjects'][s])
    subj = pzgram.create_keyboard(subj, one=False)
    shared['keyboards'] = {'days': days, 'this_m': this_m, 'next_m': next_m, 'all_month': all_month,
                           'days_c': days_c, 'this_m_c': this_m_c, 'next_m_c': this_m_c, 'subj': subj}


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


def start_action(shared):
    shared['status'] = ''
    shared['data_cache'] = {}
    shared['subjects'] = {'Math': 'Math', 'Italian': 'Ita', 'English': 'Eng', 'Systems': 'Sys', 'TPS': 'TPS',
                          'History': 'Hist', 'Gymnastic': 'Gym', 'Telecommunications': 'Tele'}

bot.set_commands({'/newtest': new_test_1, '/calendar': view_calendar, '/newhw': new_homework})  # Change with keyboard
bot.set_function({'start_action': start_action, 'after_division': process_message})
bot.set_timers({7200: allert_timer, 43200: set_keyboard})
bot.run()
