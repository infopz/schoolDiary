import pzgram
from datetime import datetime, timedelta

import SQL_function
import apiKey
import useful_function

bot = pzgram.Bot(apiKey.apiBot)

# IDEA
# TODO: MORE EMOJI!!!!!
# Subjects Emoji


def start_command(chat, message):
    chat.send('Hi, *'+message.sender.first_name+'*\n'
              'Welcome to schoolDiaryBot, \nUse the keyboard to view all the possible commands\n'
              'This is an [open-source bot](http://github.com/infopz/pzGram_schoolDiary) by @infopz\n'
              'If you want more info about this bot visit [my site](http://infopz.hopto.org/schoolDiary/)',
              disable_preview=True)

# START /new FUNCTION


def new_test(chat, shared):
    chat.send('Select a date:', reply_markup=shared['keyboards']['this_m_test'])
    shared['cache'] = {'conv_dict': shared['keyboards']['this_m_c']}
    shared['status'] = 'newTest'


def new_homework(chat, shared):
    chat.send('Select a date:', reply_markup=shared['keyboards']['days'])
    shared['cache'] = {'conv_dict': shared['keyboards']['days_c']}
    shared['status'] = 'newHW'


def manage_date(message, chat, shared):  # possible input status: newHW, newTest, editDate, find2, newVote2
    k_hist = shared['k_hist']
    c_hist = shared['c_hist']
    cache = shared['cache']
    conv_dict = cache['conv_dict']
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                  'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    if message.text in conv_dict:
        cache['date'] = conv_dict[message.text]
        if shared['status'] == 'editDate':
            set_new_date(chat, cache, shared)
            return
        if shared['status'] == 'find2':
            find_gave_result(chat, cache, shared)
            return
        if shared['status'] == 'newVote2':
            new_vote_date(chat, cache, shared)
            return
        chat.send('Ok, now select a subject:', reply_markup=shared['keyboards']['subj'])
        if shared['status'] == 'newHW':
            shared['status'] = 'newHW2'
        elif shared['status'] == 'newTest':
            shared['status'] = 'newTest2'
    elif message.text == 'This Month':
        chat.send('Select a day', reply_markup=shared['keyboards']['this_m'])
        cache['conv_dict'] = shared['keyboards']['this_m_c']
        shared['cache'] = cache
        k_hist.append('this_m')
        c_hist.append('this_m_c')
    elif message.text == 'Next Month':
        chat.send('Select a day', reply_markup=shared['keyboards']['next_m'])
        cache['conv_dict'] = shared['keyboards']['next_m_c']
        shared['cache'] = cache
        k_hist.append('next_m')
        c_hist.append('newxt_m_c')
    elif message.text == 'Other':
        chat.send('Select a month', reply_markup=shared['keyboards']['all_month'])
        k_hist.append('all_month')
        c_hist.append('')
    elif message.text in month_dict:
        month = month_dict[message.text]
        key_list, conv_dict = useful_function.create_month_keyboard(month)
        keyboard = pzgram.create_keyboard(key_list, one=True)
        chat.send('Now select a day:', reply_markup=keyboard)
        cache['conv_dict'] = conv_dict
        k_hist.append('')
        c_hist.append('')
    elif message.text == 'Prev Month':
        this_m = int(datetime.now().month)
        if this_m == 1:
            prev = 12
        else:
            prev = this_m-1
        key_list, conv_dict = useful_function.create_month_keyboard(prev)
        keyboard = pzgram.create_keyboard(key_list, one=True)
        chat.send('Select a day:', reply_markup=keyboard)
        cache['conv_dict'] = conv_dict
        k_hist.append('')
        c_hist.append('')
    elif message.text == 'Back\U0001F519':
        if len(k_hist):
            k_hist.pop()
            exec("chat.send('Select a day:', reply_markup=shared['keyboards]['"+k_hist[-1]+"'])")
            c_hist.pop()
            if c_hist[-1] != '':
                exec("cache['conv_dict] = shared['keyboards]['"+c_hist[-1]+"']")
        else:
            if shared['status'] == 'newHW' or shared['status'] == 'newTest':
                chat.send('Choose a command:')
                shared['status'] = ''
            elif shared['status'] == 'find2':
                find_command(chat, shared)
            elif shared['status'] == 'newVote2':
                new_vote_command(chat, shared)
            elif shared['status'] == 'editDate':
                chat.send(shared['cache']['one_message'], reply_markup=shared['cache']['keyb'])
                shared['status'] = 'view3'
    else:
        status = shared['status']
        if status == 'newHW':
            chat.send('The day that you give me is not correct')
            new_homework(chat, shared)
        elif status == 'newTest':
            chat.send('The day that you give me is not correct')
            new_test(chat, shared)
        elif status == 'editDate' or status == 'find2':
            chat.send('The day that you give me is not correct, retry', reply_markup=shared['keyboards']['this_m_test'])
            cache['conv_dict'] = shared['keyboards']['this_m_c']
        elif status == 'newVote2':
            chat.send('The day that you give me is not correct, retry', reply_markup=shared['keyboards']['this_m_vote'])
            cache['conv_dict'] = shared['keyboards']['this_m_c']
    shared['k_hist'] = k_hist
    shared['c_hist'] = c_hist
    shared['cache'] = cache


def manage_subject(message, chat, shared):
    cache = shared['cache']
    subjects = shared['subjects']
    if message.text == 'Back\U0001F519':
        if shared['status'] == 'newHW2':
            new_homework(chat, shared)
        elif shared['status'] == 'newTest2':
            new_test(chat, shared)
        else:  # editSubj
            chat.send(shared['cache']['one_message'], reply_markup=shared['cache']['keyb'])
            shared['status'] = 'view3'
        return
    for i in subjects:
        if subjects[i] == message.text:
            cache['subject'] = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Nice, now select the subject:", reply_markup=shared['keyboards']['subj'])
    if shared['status'] == 'editSubj':
        set_new_subj(chat, cache, shared)
        return
    s = 'Ok, last step, send me the notes about this homework:'
    if shared['status'] == 'newTest2':
        s = 'Ok, last step, send me the arguments of this test'
    chat.send(s, no_keyboard=True)
    if shared['status'] == 'newHW2':
        shared['status'] = 'newHW3'
    elif shared['status'] == 'newTest2':
        shared['status'] = 'newTest3'
    shared['cache'] = cache


def manage_args_notes(message, chat, shared):
    cache = shared['cache']
    if shared['status'] == 'newHW3':
        SQL_function.add_new_homework(cache['subject'], cache['date'], message.text)
        chat.send("Homework added to your diary")
    elif shared['status'] == 'newTest3':
        text = message.text.split('\n', 1)
        if len(text) == 2:
            SQL_function.add_new_test(cache['subject'], cache['date'], text[0], text[1])
        else:
            SQL_function.add_new_test(cache['subject'], cache['date'], text[0])
        chat.send("Test added to your diary")
    shared['cache'] = {}
    shared['status'] = ''

# END /new FUNCION
# START /view FUNCTION


def view_calendar(chat, shared):
    keyboard = pzgram.create_keyboard([['This Week', 'Next Week'], ['This Month', 'Next Month'], ['Other', 'Back\U0001F519']],
                                      one=True)
    chat.send('Select a period', reply_markup=keyboard)
    shared['status'] = 'view'


def view_manage_date(message, chat, shared):
    if message.text == 'Back\U0001F519':
        chat.send('Select a command:')
        return
    start_date, stop_date = '', ''
    month_length = [00, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if message.text == 'This Week':
        start_date = datetime.now().strftime('%m%d')
        stop_date = (datetime.now() + timedelta(days=(7-int(datetime.now().strftime('%u'))))).strftime('%m%d')
    elif message.text == 'Next Week':
        start_date = (datetime.now() + timedelta(days=(8-int(datetime.now().strftime('%u'))))).strftime('%m%d')
        stop_date = (datetime.strptime(start_date, '%m%d') + timedelta(days=6)).strftime('%m%d')
    elif message.text == 'This Month':
        start_date = datetime.now().strftime('%m%d')
        this_m = datetime.now().strftime('%m')
        stop_date = this_m+str(month_length[int(this_m)])
    elif message.text == 'Next Month':
        this_m = datetime.now().month
        next_m = (datetime.now() + timedelta(days=month_length[int(this_m)])).strftime('%m')
        start_date = next_m + '01'
        stop_date = next_m + str(month_length[int(next_m)])
    if start_date != '' and stop_date != '':
        m, k, conv_dict = useful_function.view_tasks_between(start_date, stop_date)
        if m == '':
            m = 'You have no tasks in this period, select another one'
            keyboard = pzgram.create_keyboard(
                [['This Week', 'Next Week'], ['This Month', 'Next Month'], ['Other', 'Back\U0001F519']], one=True)
            chat.send(m, reply_markup=keyboard)
        else:
            chat.send(m, reply_markup=k)
            shared['cache'] = {'conv_dict': conv_dict, 'comm_keyb': k, 'message': m}
            shared['status'] = 'view2'


def view_one(message, chat, shared):
    if message.text == 'Back\U0001F519':
        view_calendar(chat, shared)
        return
    cache = shared['cache']
    if message.text not in cache['conv_dict']:
        chat.send('Error, please select another one', reply_markup=cache['comm_keyb'])
        return
    row = cache['conv_dict'][message.text]
    if row[0] == 't':
        test = SQL_function.get_one_row('Test', row[1:])
        m = '*' + test[0] + ' Test*\n'
        year = '2018'
        if int(test[1][0:2]) >= 7:
            year = '2017'
        date = datetime.strptime(test[1]+year, '%m%d%Y').strftime('%a %d %b')  # Ex. Mon 12 Feb
        m += date + '\n'
        m += test[2] + '\n'
        keyboard = [['Menu\U0001F3B2', 'Edit Date'], ['Edit Subj', 'Edit Arg', 'Edit Notes'], ['Back\U0001F519']]
        if test[3] is not None:
            m += test[3]
        keyboard = pzgram.create_keyboard(keyboard, one=True)
        chat.send(m, reply_markup=keyboard)
        cache['one_message'] = m
        shared['status'] = 'view3'
        cache['keyb'] = keyboard
        cache['row'] = row
    elif row[0] == 'h':
        hw = SQL_function.get_one_row('Homework', row[1:])
        m = '*' + hw[0] + ' Homework*\n'
        year = '2018'
        if int(hw[1][0:2]) >= 7:
            year = '2017'
        date = datetime.strptime(hw[1] + year, '%m%d%Y').strftime('%a %d %b')  # Ex. Mon 12 Feb
        m += date + '\n'
        m += hw[2] + '\n'
        keyboard = [['Menu\U0001F3B2', 'Completed\U00002611'], ['Edit Date', 'Edit Subj', 'Edit Notes'], ['Back\U0001F519']]
        if hw[3]:
            m += '_Completed\U00002611_'
            keyboard = [['Menu\U0001F3B2', 'Back\U0001F519'], ['Edit Date', 'Edit Subj', 'Edit Notes']]
        keyboard = pzgram.create_keyboard(keyboard, one=True)
        chat.send(m, reply_markup=keyboard)
        cache['one_message'] = m
        shared['status'] = 'view3'
        cache['keyb'] = keyboard
        cache['row'] = row
    shared['cache'] = cache


def view_edit_one(message, chat, shared):
    if message.text == 'Back\U0001F519':
        chat.send(shared['cache']['message'], reply_markup=shared['cache']['comm_keyb'])
        shared['status'] = 'view2'
        return
    cache = shared['cache']
    possible_options = ['Edit Date', 'Edit Subj', 'Edit Arg', 'Edit Notes', 'Completed\U00002611']
    if message.text not in possible_options:
        chat.send('Error Command, try another', reply_markup=cache['keyb'])
        return
    row = cache['row']
    if row[0] == 't':
        c_type = 'test'
    else:
        c_type = 'hw'
    if message.text == 'Edit Date':
        if c_type == 'test':
            keyboard = shared['keyboards']['this_m_test']
            cache['conv_dict'] = shared['keyboards']['this_m_c']
        else:
            keyboard = shared['keyboards']['days']
            cache['conv_dict'] = shared['keyboards']['days_c']
        chat.send('Select a new date', reply_markup=keyboard)
        shared['cache'] = cache
        shared['status'] = 'editDate'
    elif message.text == 'Edit Subj':
        keyboard = shared['keyboards']['subj']
        chat.send('Select a new subject', reply_markup=keyboard)
        shared['status'] = 'editSubj'
    elif message.text == 'Edit Arg':
        if c_type == 'hw':
            return
        chat.send('Give me the new arguments', no_keyboard=True)
        shared['status'] = 'editArg'
    elif message.text == 'Edit Notes':
        chat.send('Give me the new notes', no_keyboard=True)
        shared['status'] = 'editNotes'
    elif message.text == 'Completed\U00002611':
        if c_type == 'test':
            return
        SQL_function.update_value('Homework', row[1:], 'Finished', 1)
        chat.send('Homework set as Completed\U00002611')


def set_new_date(chat, cache, shared):
    row = cache['row']
    date = cache['date']
    if row[0] == 't':
        SQL_function.update_value('Test', row[1:], 'Date', date)
    else:
        SQL_function.update_value('Homework', row[1:], 'Date', date)
    chat.send('Date updated')
    shared['cache'] = {}
    shared['status'] = ''


def set_new_subj(chat, cache, shared):
    row = cache['row']
    subj = cache['subject']
    if row[0] == 't':
        SQL_function.update_value('Test', row[1:], 'Subject', subj)
    else:
        SQL_function.update_value('Homework', row[1:], 'Subject', subj)
    chat.send('Subject updated')
    shared['cache'] = {}
    shared['status'] = ''


def set_new_arg(message, chat, shared):
    new_arg = message.text
    row = shared['cache']['row'][1:]
    SQL_function.update_value('Test', row, 'Arguments', new_arg)
    chat.send('Arguments updated')


def set_new_notes(message, chat, shared):
    new_notes = message.text
    row = shared['cache']['row']
    if row[0] == 't':
        SQL_function.update_value('Test', row[1:], 'Notes', new_notes)
    else:
        SQL_function.update_value('Homework', row[1:], 'Notes', new_notes)
    chat.send('Notes updated')

# END /view FUNCTION
# START /find FUNCTION


def find_command(chat, shared):
    keyboard = pzgram.create_keyboard([['Homeworks', 'Tests'], ['Both'], ['Menu\U0001F3B2', 'Back\U0001F519']], one=True)
    chat.send('Select wich type of tasks you want to find:', reply_markup=keyboard)
    shared['cache'] = {}
    shared['status'] = 'find1'


def find_ask_date(message, chat, shared):  # TODO: bold the day with tasks
    if message.text == 'Back\U0001F519':
        chat.send('Choose a command:')
        return
    options = ['Homeworks', 'Tests', 'Both']
    if message.text not in options:
        keyboard = pzgram.create_keyboard([['Homeworks', 'Tests'], ['Both']], one=True)
        chat.send("Select a type from the keyboard:", reply_markup=keyboard)
        return
    cache = shared['cache']
    cache['option'] = message.text
    chat.send('Now select a date:', reply_markup=shared['keyboards']['this_m_test'])
    cache['conv_dict'] = shared['keyboards']['this_m_c']
    shared['status'] = 'find2'
    shared['cache'] = cache


def find_gave_result(chat, cache, shared):
    date = cache['date']
    test, hw = SQL_function.find_one_day(date)
    if not len(test) and not len(hw):  # if nothing
        chat.send("You don't have nothing for this day")
        return
    m = "Here's your commintments:\n"
    if len(test):
        for t in test:
            m += '*'+t[1]+"'s Test*\n"
            m += t[2]+'\n'
            if t[3] is not None:
                m += t[3]+'\n'
    if len(hw):
        for h in hw:
            m += '*' + h[1] + "'s Homeworkt*\n"
            m += t[2] + '\n'
            if t[3]:
                m += '_Completed\U00002611_' + '\n'
    chat.send(m)
    shared['status'] = ''
    shared['cache'] = {}

# END /find FUNCTIONS
# START /newvote FUNCTIONS


def new_vote_command(chat, shared):
    shared['status'] = 'newVote'
    shared['cache'] = {}
    chat.send('Write me the vote:', no_keyboard=True)


def new_vote_number(message, chat, shared):
    cache = shared['cache']
    try:
        cache['number'] = float(message.text)
    except ValueError:
        chat.send('The number inserted was not correct')
        new_vote_command(chat, shared)
        return
    chat.send('Now send me the date of this test', reply_markup=shared['keyboards']['this_m_test'])
    cache['conv_dict'] = shared['keyboards']['this_m_c']
    shared['status'] = 'newVote2'
    shared['cache'] = cache


def new_vote_date(chat, cache, shared):
    chat.send('Ok, now send me the subject', reply_markup=shared['keyboards']['subj'])
    shared['cache'] = cache
    shared['status'] = 'newVote3'


def new_vote_subj(message, chat, shared):
    if message.text == 'Back\U0001F519':
        chat.send('Now send me the date of this test', reply_markup=shared['keyboards']['this_m_test'])
        shared['cache']['conv_dict'] = shared['keyboards']['this_m_c']
        shared['status'] = 'newVote2'
        return
    subj = shared['subjects']
    cache = shared['cache']
    for i in subj:
        if subj[i] == message.text:
            cache['subject'] = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Select the subject:", reply_markup=shared['keyboards']['subj'])
        return
    keyboard = pzgram.create_keyboard([['Written', 'Oral'], ['Practice']], one=True)
    chat.send('Select the kind of this vote:', reply_markup=keyboard)
    shared['cache'] = cache
    shared['status'] = 'newVote4'


def new_vote_type(message, chat, shared):
    if message.text == 'Back\U0001F519':
        chat.send('Ok, now send me the subject', reply_markup=shared['keyboards']['subj'])
        shared['status'] = 'newVote3'
        return
    if message.text not in ['Written', 'Oral', 'Practice']:
        keyboard = pzgram.create_keyboard([['Written', 'Oral'], ['Practice']], one=True)
        chat.send('Select the kind of this vote:', reply_markup=keyboard)
        return
    cache = shared['cache']
    cache['type'] = message.text
    keyboard = pzgram.create_keyboard([['Yes', 'No']], one=True)
    chat.send('Do you want to add some notes to this vote?', reply_markup=keyboard)
    shared['cache'] = cache
    shared['status'] = 'newVote5'


def new_vote_notes_ask(message, chat, shared):
    if message.text not in ['Yes', 'No']:
        chat.send('You only answer me with *yes* or *no*')
        keyboard = pzgram.create_keyboard([['Yes', 'No']], one=True)
        chat.send('Do you want to add some notes to this vote?', reply_markup=keyboard)
        return
    if message.text == 'Yes':
        chat.send('Ok, send me the notes to attach at this vote', no_keyboard=True)
        shared['status'] = 'newVote6'
    else:
        cache = shared['cache']
        SQL_function.add_new_vote(cache['number'], cache['subject'], cache['type'], cache['date'])
        chat.send('Vote added')
        shared['status'] = ''


def new_vote_notes_receive(message, chat, shared):
    cache = shared['cache']
    SQL_function.add_new_vote(cache['number'], cache['subject'], cache['type'], cache['date'], message.text)
    chat.send('Vote added')
    shared['status'] = ''

# END /newvote FUNCTIONS
# START /viewvotes FUNCTIONS


def view_vote_command(chat, shared):
    keyboard = pzgram.create_keyboard([['Date', 'Subject'], ['Average'], ['Menu\U0001F3B2', 'Back\U0001F519']])
    chat.send('Select an option:', reply_markup=keyboard)
    shared['status'] = 'viewVotes'


def view_vote_answer(message, chat, shared):
    if message.text == 'Back\U0001F519':
        chat.send('Choose a command:')
        return
    if message.text not in ['Date', 'Subject', 'Average']:
        keyboard = pzgram.create_keyboard([['Date', 'Subject'], ['Average']])
        chat.send('You give me a bad answer, please select an option:', reply_markup=keyboard)
        return
    if message.text == 'Date':
        convert_type = {'Practice': 'P', 'Oral': 'O', 'Written': 'W'}
        votes = SQL_function.get_vote_date()
        m = "Here's your votes:\n"
        for i in votes:
            subj = i[2]
            subj = shared['subjects'][subj]
            m += f'{i[0]} - {subj} {convert_type[i[3]]} - {i[1][0:2]}/{i[1][2:4]}\n'
        chat.send(m)
        shared['status'] = ''
        shared['cache'] = {}
    elif message.text == 'Subject':
        chat.send('Select a subject', reply_markup=shared['keyboards']['subj'])
        shared['status'] = 'viewVotesSubj'
    else:
        keyboard = pzgram.create_keyboard([['With Type', 'All votes']])
        chat.send('Select a type:', reply_markup=keyboard)
        shared['status'] = 'viewVotesAvg'


def view_vote_subj(message, chat, shared):
    subj = shared['subjects']
    for i in subj:
        if subj[i] == message.text:
            sel_subject = i
            break
    else:
        chat.send('The subject that you chose is not correct, retry')
        chat.send("Select the subject:", reply_markup=shared['keyboards']['subj'])
        return
    votes = SQL_function.get_vote_subj(sel_subject)
    if len(votes):
        convert_type = {'Practice': 'Pr', 'Oral': 'Or', 'Written': 'Wr'}
        m = ''
        for v in votes:
            m += f'{v[0]} -  {convert_type[v[1]]} - {v[2][0:2]}/{v[2][2:4]}\n'
            if v[3] is not None:
                m += '   ' + v[3] + '\n'
        chat.send(m)
    else:
        chat.send('You have no vote for this subject')
    shared['status'] = ''
    shared['cache'] = {}


def view_vote_average(message, chat, shared):
    if message.text not in ['With Type', 'All votes']:
        keyboard = pzgram.create_keyboard([['With Type', 'All votes']])
        chat.send('Please, select a valid type:', reply_markup=keyboard)
        return
    if message.text == 'With Type':
        avg = SQL_function.get_average(True)
        convert_type = {'Practice': 'Pr', 'Oral': 'Or', 'Written': 'Wr'}
        m = "Here's your averages:"
        for i in avg:
            m += i[0] + ' - ' + shared['subject'][i[1]] + ' ' + convert_type[i[2]] + '\n'
        chat.send(m)
    else:
        avg = SQL_function.get_average(False)
        m = "Here's your averages:"
        for i in avg:
            m += i[0] + ' - ' + shared['subject'][i[1]] + ' ' + '\n'
        chat.send(m)
    shared['status'] = ''
    shared['cache'] = ''

# END /viewvotes FUNCTIONS
# START /loadtimes FUNCTIONS


def load_times(chat, shared):
    try:
        shared['times'] = useful_function.load_times()
        chat.send('School Times loaded')
    except Exception as e:
        print('Error while loading - ' + str(e))

# END /loadtimes FUNCTIONS
# START /viewtimes FUNCTIONS


def view_times_command(chat, shared):
    day_keyboard = pzgram.create_keyboard([['Mon', 'Tue', 'Wed'], ['Thr', 'Fri', 'Sat']], one=True)
    chat.send("Select a day:", reply_markup=day_keyboard)
    shared['status'] = 'times'


def view_times_send(message, chat, shared):
    if message.text not in ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat']:
        day_keyboard = pzgram.create_keyboard([['Mon', 'Tue', 'Wed'], ['Thr', 'Fri', 'Sat']], one=True)
        chat.send("Please, select one of this day:", reply_markup=day_keyboard)
        return
    convert_dict = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thr': 3, 'Fri': 4, 'Sat': 5}
    number_day = convert_dict[message.text]
    times = shared['times']
    subjects = times['days'][number_day]['subjects']
    m = ''
    for n, s in enumerate(subjects, start=1):
        m += str(n) + ' ' + s + '\n'
    chat.send(m)
    shared['status'] = ''

# END /viewtimes FUNCTIONS


def allert_timer(bot, shared):
    h = int(datetime.now().strftime('%H'))
    if h == 14:
        print("Timer 14")
        s = useful_function.check_tomorrow()
        if s != '':
            pzgram.Chat(20403805, bot).send(s)
    elif h == 20:
        print("Timer 20")
        tomorrow = int((datetime.now()+timedelta(days=1)).strftime('%u')) - 1
        if tomorrow != 6:
            times = shared['times']
            subjects = times['days'][tomorrow]['subjects']
            m = ''
            for n, s in enumerate(subjects, start=1):
                m += str(n) + ' ' + s + '\n'
            pzgram.Chat(20403805, bot).send("Dear Egg\nHere's your subjects for tomorrow")
            pzgram.Chat(20403805, bot).send(m)


def set_keyboard(shared):
    month = int(datetime.now().strftime('%m'))
    days_l, days_c = useful_function.create_hw_keyboard()  # 'Default Keyboard'
    this_m_l, this_m_c = useful_function.create_this_month_keyboard()  # All days of this m
    next_m_l, next_m_c = useful_function.create_month_keyboard(month+1)  # All days of next m
    days = pzgram.create_keyboard(days_l, one=True)
    this_m = pzgram.create_keyboard(this_m_l, one=True)
    this_m_test_l = this_m_l.copy()
    this_m_test_l.insert(-1, ['Next Month', 'Other'])
    this_m_vote_l = this_m_l.copy()
    this_m_vote_l.insert(-1, ['Prev Month', 'Other'])
    this_m_vote = pzgram.create_keyboard(this_m_vote_l, one=True)  # Like this month, with prev button
    this_m_test = pzgram.create_keyboard(this_m_test_l, one=True)  # Like this month, with buttons
    next_m = pzgram.create_keyboard(next_m_l, one=True)
    all_month = pzgram.create_keyboard(useful_function.create_all_month_keyboard(), one=True)
    subj = [[], [], []]
    for i, s in enumerate(shared['subjects']):
        subj[i // 3].append(shared['subjects'][s])
    subj.append(['Menu\U0001F3B2', 'Back\U0001F519'])
    subj = pzgram.create_keyboard(subj, one=False)
    shared['keyboards'] = {'days': days, 'this_m': this_m, 'next_m': next_m, 'all_month': all_month,
                           'this_m_test': this_m_test, 'days_c': days_c, 'this_m_c': this_m_c,
                           'next_m_c': next_m_c, 'subj': subj, 'this_m_vote': this_m_vote}


def process_message(message, chat, shared):
    print(message.text)
    text_dict = shared['text_dict']
    status_dict = shared['status_dict']
    if message.text == 'Menu\U0001F3B2' or message.text == 'Menu':
        chat.send('Choose a command:')
        shared['status'] = ''
    elif message.text in text_dict:
        text_dict[message.text](chat, shared)
    elif shared['status'] in status_dict:
        status_dict[shared['status']](message, chat, shared)


def start_action(shared):
    shared['status'] = ''
    shared['cache'] = {}
    shared['subjects'] = {'Math': 'Math', 'Italian': 'Ita', 'English': 'Eng', 'Systems': 'Sys', 'TPS': 'TPS',
                          'Telecom': 'Tele', 'History': 'Hist', 'Phis. Edication': 'PE', 'GPI': 'GPI'}
    shared['text_dict'] = {'View': view_calendar, 'Find': find_command, 'New Test': new_test,
                           'New Homework': new_homework, 'New Vote': new_vote_command, 'View Vote': view_vote_command,
                           'View Times': view_times_command}
    shared['status_dict'] = {'newHW': manage_date, 'newHW2': manage_subject, 'newHW3': manage_args_notes,
                             'newTest': manage_date, 'newTest2': manage_subject, 'newTest3': manage_args_notes,
                             'view': view_manage_date, 'view2': view_one, 'view3': view_edit_one,
                             'editDate': manage_date, 'editSubj': manage_subject, 'editArg': set_new_arg,
                             'editNotes': set_new_notes, 'find1': find_ask_date, 'find2': manage_date,
                             'newVote2': manage_date, 'newVote3': new_vote_subj, 'newVote4': new_vote_type,
                             'newVote5': new_vote_notes_ask, 'newVote6': new_vote_notes_receive,
                             'viewVotes': view_vote_answer, 'viewVotesSubj': view_vote_subj,
                             'viewVotesAvg': view_vote_average, 'newVote': new_vote_number, 'times': view_times_send}
    shared['k_hist'] = []
    shared['c_hist'] = []
    shared['times'] = useful_function.load_times()

bot.set_commands({'/newtest': new_test, '/view': view_calendar, '/newhw': new_homework, '/start': start_command,
                  '/find': find_command, '/newvotes': new_vote_command, '/viewvotes': view_vote_command,
                  '/loadtimes': load_times, '/viewtimes': view_times_command})
bot.set_function({'start_action': start_action, 'after_division': process_message})
bot.set_timers({3600: allert_timer, 43200: set_keyboard})
bot.set_keyboard([['View', 'Find'], ['New Test', 'New Homework'], ['New Vote', 'View Vote'],['View Times']])
bot.run()
