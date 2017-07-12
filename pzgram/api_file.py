import requests
import time
from .ExceptionFile import *


def api_request(key, method, p=None):
    while True:
        try:
            data = requests.get(f"https://api.telegram.org/bot{key}/{method}", params=p)
        except Exception as e:
            print('Request error - ' + str(e))
            raise ApiError
        status_code = data.status_code
        data = data.json()
        if status_code == 200:
            return data
        else:
            action, data = recognize_error(status_code, data)
            if action == 'continue':
                raise ApiError
            elif action == 'stop':
                raise StopBot(data)
            elif action == 'retry':
                time.sleep(data)


def recognize_error(code, data):
    error_description = ''
    try:
        error_description = data['description']
    except KeyError:
        pass
    if code == 400:
        print('API_Request - BadRequest Error ' + error_description)
        return 'continue', None
    elif code == 401:
        print('API_Request - BotKey Error ' + error_description)
        return 'stop', 'API_Request - BotKey Error ' + error_description
    elif code == 403:
        print('API_Request - Privacy Error ' + error_description)
        return 'continue', None
    elif code == 404:
        print('API_Request - NotFound Error ' + error_description)
        return 'continue', None
    elif code == 409:
        print('API_Request - AnotherInstance Error - Retry in 3s')
        return 'retry', 3
    elif code == 420:
        second = error_description.split('_')[2]  # FLOOD_WAIT_X
        print('API_Request - TooMuchMessage Error - Retry in ' + second)
        return 'retry ', int(second)
    elif code == 500:
        print('API_Request - TelegramInternal Error')
        return 'continue'
    else:
        print('API_Request - Unknown Error ' + error_description)
        return 'continue'
