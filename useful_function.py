from datetime import datetime, timedelta


def convert_month(month):
    month_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                  'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    try:
        return month_dict[month]
    except IndexError:
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


def subtract_days(date, n_days):
    date_formatted = datetime.strptime(str(date) + '2018', "%d%m%Y")
    date_new = date_formatted - timedelta(days=int(n_days))
    return date_new.strftime('%d%m')
