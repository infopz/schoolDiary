from datetime import datetime, timedelta
import json
import SQL_function


def convert_month(month):
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                  'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    try:
        return month_dict[month]
    except KeyError:
        return ''


def create_date(day, month):
    month = str(month)
    if len(month) == 1:  # trasform 5 in 05
        month = "0" + month
    day = str(day)
    if len(day) == 1:
        day = "0" + day
    return month+day


def modify_days(date, n_days, operation=True):  # True -> Add, False -> Sub
    date_formatted = datetime.strptime(str(date) + '2018', "%m%d%Y")
    if operation:
        date_new = date_formatted + timedelta(days=int(n_days))
        return date_new.strftime('%m%d')
    else:
        date_new = date_formatted - timedelta(days=int(n_days))
        return date_new.strftime('%m%d')


def convert_test_all(t):  # call only with date
    if t[3] is not None:
        return '*' + t[1] + ' test*\n' + t[2] + ' - ' + t[3] + ' \n'
    else:
        return '*' + t[1] + ' test*\n' + t[2] + '\n'


def convert_homework_all(h):
    return '*' + h[1] + ' homework*\n' + h[2] + '\n'


def check_tomorrow():
    date = datetime.now().strftime('%m%d')
    tomorrow = modify_days(date, 1)
    test, homeworks = SQL_function.find_one_day(tomorrow)
    not_compl_homeworks = []
    if len(homeworks) != 0:
        for i in range(len(homeworks)):
            if homeworks[i][2] == 0:
                not_compl_homeworks.append(homeworks[i])
    if len(test) == 0 and len(not_compl_homeworks) == 0:
        return ''
    s = ''
    if len(test) != 0:
        s += 'Ehi, you have a test tomorrow!\n'
        for i in test:
            if i[2] is not None:
                s += '*'+i[0] + ' test*\n' + i[1] + ' - ' + i[2] + ' \n'
            else:
                s += '*' + i[0] + ' test*\n' + i[1] + '\n'
    if len(not_compl_homeworks) != 0:
        if s != '':
            s += '\nAnd you also have homeworks:\n'
        else:
            s += 'Ehi, you have some homeworks for tomorrow!\n'
        for h in not_compl_homeworks:
            s += '*' + h[0] + ' homework*\n' + h[1] + '\n'
    return s


def create_hw_keyboard():
    week_list = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    correspond_dict = {}
    keyboard = list()
    now = datetime.now()
    now_date = now.strftime('%m%d')
    keyboard.append(['Tomorrow'])
    correspond_dict['Tomorrow'] = modify_days(now_date, 1)
    effective_increment = 2
    keyboard.append([])
    for i in range(1, 6):
        next_day = now + timedelta(days=effective_increment)
        if next_day.strftime('%u') == '7':
            effective_increment += 1
            next_day = now + timedelta(days=effective_increment)
        day_n = week_list[int(next_day.strftime('%u'))-1]
        button = day_n+' '+next_day.strftime('%d')
        keyboard[1].append(button)
        correspond_dict[button] = modify_days(now_date, effective_increment)
        effective_increment += 1
    keyboard.append(['This Month', 'Next Month', 'Other'])
    keyboard.append(['Menu\U0001F3B2', 'Back\U0001F519'])
    return keyboard, correspond_dict


def create_month_keyboard(month):
    week_list = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
    month = str(month)
    if len(month) == 1:  # trasform 5 in 05
        month = "0" + month
    year = 2018
    if int(month) > 7:
        year = 2017
    keyboard = [[]]
    conversion_dict = {}
    month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    row = 0
    first_day = datetime.strptime(str(year)+month+'01', '%Y%m%d')
    for i in range(1, month_length[int(month)-1]+1):
        day = first_day+timedelta(days=i-1)
        d_week = int(day.strftime('%u'))-1
        if d_week == 6:
            if i != 1:
                row += 1
                keyboard.append([])
            continue
        d_week = week_list[int(day.strftime('%u'))-1]
        button = d_week + ' ' + str(i)
        keyboard[row].append(button)
        conversion_dict[button] = day.strftime('%m%d')
    keyboard.append(['Menu\U0001F3B2', 'Back\U0001F519'])
    return keyboard, conversion_dict


def create_this_month_keyboard():
    month = int(datetime.now().strftime('%m'))
    week_list = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
    keyboard = [[]]
    conversion_dict = {}
    month_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    row = 0
    first_day = datetime.now()
    for i in range(1, month_length[int(month) - 1] - int(first_day.strftime('%d'))):
        day = first_day + timedelta(days=i - 1)
        d_week = int(day.strftime('%u')) - 1
        if d_week == 6:
            if i != 1:
                row += 1
                keyboard.append([])
            continue
        d_week = week_list[int(day.strftime('%u')) - 1]
        button = d_week + ' ' + day.strftime('%d')
        keyboard[row].append(button)
        conversion_dict[button] = day.strftime('%m%d')
    keyboard.append(['Menu\U0001F3B2', 'Back\U0001F519'])
    return keyboard, conversion_dict


def create_all_month_keyboard():
    month = int(datetime.now().strftime('%m')) - 1
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    keyboard = [[], [], []]
    reset = 0
    for i in range(12):
        if month + i > 11:
            keyboard[i//4].append(month_list[reset])
            reset += 1
        else:
            keyboard[i//4].append(month_list[month + i])
    return keyboard


def load_times():
    return json.loads(open('times.json', 'r').read())


def view_commitments_between(start, stop):
    tests, homeworks = SQL_function.find_between(start, stop)
    s = ''
    current_date = start
    keyboard = []
    conv_dict = {}
    row = -1
    while True:
        smt_found = False  # something
        year = '18'
        if int(start[0:2]) >= 7:
            year = '17'
        current_day = datetime.strptime(current_date + year, '%m%d%y').strftime('%a')
        formatted_date = current_date[2:4] + '/' + current_date[0:2]
        for t in tests:
            if t[2] == current_date:
                if not smt_found:
                    smt_found = True
                    s += '*' + current_day + ' ' + formatted_date + '*\n'
                keyboard.append([])
                row += 1
                r = t[1] + ' test'
                s += r + '\n'
                keyboard[row].append(formatted_date + ' ' + r)
                conv_dict[formatted_date + ' ' + r] = 't' + str(t[0])
        for h in homeworks:
            if h[2] == current_date:
                if not smt_found:
                    smt_found = True
                    s += '*' + current_day + ' ' + formatted_date + '*\n'
                keyboard.append([])
                row += 1
                r = h[1] + ' homework'
                s += r + '\n'
                keyboard[row].append(formatted_date + ' ' + r)
                conv_dict[formatted_date + ' ' + r] = 'h' + str(h[0])
        if current_date == stop:
            break
        current_date = (datetime.strptime(current_date, '%m%d') + timedelta(days=1)).strftime('%m%d')
    keyboard.append(['Menu\U0001F3B2', 'Back\U0001F519'])
    keyboard = pzgram.create_keyboard(keyboard, one=True)
    return s, keyboard, conv_dict
