import requests
import json


def register(url, user_id):
    # url = 'wowredux.ru'
    post = {
        'user_id': {user_id}
    }
    response = requests.request('POST', url=url, json=post)
    data = json.loads(response.text)
    print(data)
    connect_user_password = data['password']

    return f'Ваш логин: {user_id}\n' \
           f'Ваш пароль: {connect_user_password}'
