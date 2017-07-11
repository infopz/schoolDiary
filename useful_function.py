from datetime import datetime, timedelta
import SQL_function


def convert_month(month):
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                  'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    try:
        return month_dict[month]
    except KeyError:
        return ''


def check_date(day, month):
    try:
        month = str(month)
        if len(month) == 1:  # trasform 5 in 05
            month = "0" + month
        day = str(day)
        if len(day) == 1:
            day = "0" + day
        datetime.strptime(day + month + '2017', "%d%m%Y")  # check for leap year (2017/2018 aren't a leap years)
        return True  # if no error
    except:
        return False


def create_date(day, month):
    month = str(month)
    if len(month) == 1:  # trasform 5 in 05
        month = "0" + month
    day = str(day)
    if len(day) == 1:
        day = "0" + day
    return day+month


def modify_days(date, n_days, operation=True):  # True -> Add, False -> Sub
    date_formatted = datetime.strptime(str(date) + '2018', "%d%m%Y")
    if operation:
        date_new = date_formatted + timedelta(days=int(n_days))
        return date_new.strftime('%d%m')
    else:
        date_new = date_formatted - timedelta(days=int(n_days))
        return date_new.strftime('%d%m')


def convert_test(test):
    return test[1][0:2] + '/' + test[1][2:4] + ' ' + test[0] + ' test'


def convert_homework(hw):
    return hw[1][0:2] + '/' + hw[1][2:4] + ' ' + hw[0] + ' homework'


def check_tomorrow():
    date = datetime.now().strftime('%d%m')
    tomorrow = modify_days(date, 1)
    test, homeworks = SQL_function.find_commitments(tomorrow)
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
            s += '*'+h[0] + ' homework*\n' + h[1] + '\n'
    return s


def create_hw_keyboard():
    week_list = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    correspond_dict = {}
    keyboard = list()
    now = datetime.now()
    now_date = now.strftime('%d%m')
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
    keyboard.append(['This Month', 'Next Month'])
    keyboard.append(['Other'])
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
        conversion_dict[button] = day.strftime('%d%m')
    return keyboard, conversion_dict

