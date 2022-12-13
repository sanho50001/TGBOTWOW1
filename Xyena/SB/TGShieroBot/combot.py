import requests
import json
import datetime
import time
import config
import history
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

class User:
    def __init__(self):
        self.country = ''
        self.city = ''
        self.hostels = ''

        self.min_money = ''
        self.max_money = ''

        self.number_hostels = ''
        self.reply = ''
        self.mode = ''

        self.day_in = ''
        self.month_in = ''
        self.year_in = ''

        self.day_out = ''
        self.month_out = ''
        self.year_out = ''

    def set_country(self, country: str):
        self.country = country

    def set_city(self, city: str):
        self.city = city
        
    def set_hostels(self, hostels: str):
        self.hostels = hostels

    def set_max_money(self, max_money: int):
        self.max_money = max_money

    def set_min_money(self, min_money: int):
        self.min_money = min_money

    def set_number_hostels(self, number_hostels: int):
        self.number_hostels = number_hostels

    def set_need_photo(self, reply: str):
        self.reply = reply

    def set_mode(self, mode: str):
        self.mode = mode

    # def set_day(self, day: str):
    #     self.day = day
    #
    # def set_month(self, month: str):
    #     self.month = month
    #
    # def set_year(self, year: str):
    #     self.year = year

    def set_datetime_in(self, day, month, year):
        self.day_in = day
        self.month_in = month
        self.year_in = year

    def set_datetime_out(self, day, mount, year):
        self.day_out = day
        self.month_out = mount
        self.year_out = year

    def get_country(self):
        return self.country
    
    def get_city(self):
        return self.city

    def get_hostels(self):
        return self.hostels

    def get_max_money(self):
        return self.max_money

    def get_min_money(self):
        return self.min_money

    def get_number_hostels(self):
        return self.number_hostels

    def get_need_photo(self):
        return self.reply

    def get_mode(self):
        return self.mode

    def get_day_in(self):
        return self.day_in

    def get_month_in(self):
        return self.month_in

    def get_year_in(self):
        return self.year_in

    def get_day_out(self):
        return self.day_out

    def get_month_out(self):
        return self.month_out

    def get_year_out(self):
        return self.year_out




class CommandsTelegram:
    print(f'Бот был запущен в', datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S'))

    def __init__(self, bot):
        self.bot = bot
        self.user_data = User()
        self.history = history.DataBase(user_id=self.user_data)

    def set_city(self, message):
        print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} '
              f'{message.from_user.last_name}: {message.text}')

        self.user_data.set_city(city=message.text)
        self.history.set_request(request=self.user_data.get_city())

        self.bot.send_message(message.from_user.id, config.b_ask_num_hostel)
        print(f'Ответ бота: {config.b_ask_num_hostel}')
        print()

        self.bot.register_next_step_handler(message, self.ask_number_hostels)

    def ask_number_hostels(self, message):

        print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')

        if isinstance(message.text, int) > int(10):
            self.bot.send_message(message, config.b_say_max_num_hostel)
            print(f'Ответ бота: {config.b_say_max_num_hostel}')
            self.bot.register_next_step_handler(message, self.ask_number_hostels)

        else:
            self.user_data.set_number_hostels(message.text)
            self.bot.send_message(message.from_user.id, config.b_ask_need_photo)
            print(f'Ответ бота: {config.b_ask_need_photo}')
            self.bot.register_next_step_handler(message, self.ask_need_photo)

    def ask_need_photo(self, message):
        print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
        self.bot.send_message(message.from_user.id, 'Еще раз повторите')
        print(f'Ответ бота: Еще раз повторите')
        # совет, откажись от приведения типов и try except, сделай проверку на тип и верни ошибку

        if message.text == 'Да' or 'да':
            self.user_data.set_need_photo('YES')
            self.bot.register_next_step_handler(message, self.info)

        elif message.text == 'Нет' or 'нет':
            self.user_data.set_need_photo('NO')
            self.bot.register_next_step_handler(message, self.info)

            #не доделанная логика еще
        else:
            print(config.b_say_what)
            self.bot.send_message(message, config.b_say_what)


    def info(self, message):

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": f"{self.user_data.get_city()}", "locale": f"en_US", "langid": f"1033",
                       "siteid": f"300000001"}
        headers = {
            "X-RapidAPI-Key": "a4a48b383fmsh7fc727029fd5ed8p19882cjsn51fd4f2b505e",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)


        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000032,
            "destination": {"regionId": f"{data['sr'][1]['gaiaId']}"},
            "checkInDate": {
                "day": 1,
                "month": 1,
                "year": 2023
            },
            "checkOutDate": {
                "day": 10,
                "month": 1,
                "year": 2023
            },
            "rooms": [
                {
                    "adults": 2
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 200,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {
                "max": 150,
                "min": 100
            }}
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "a4a48b383fmsh7fc727029fd5ed8p19882cjsn51fd4f2b505e",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        data = json.loads(response.text)

        name = data['data']['propertySearch']['properties'][0]['name']
        count = data['data']['propertySearch']['properties'][0]['mapMarker']['label']
        latitude = data['data']['propertySearch']['properties'][0]['mapMarker']['latLong']['latitude']
        longtidude = data['data']['propertySearch']['properties'][0]['mapMarker']['latLong']['longitude']
        url_photo = data['data']['propertySearch']['properties'][0]['propertyImage']['image']['url']
        text = f'Название отеля {name}, стоимость {count}, местоположение {latitude},{longtidude}, фото {url_photo}'
        self.bot.send_message(message.from_user.id, text)

    def info_highprice(self, message):
        print()

        try:
            url = "https://hotels4.p.rapidapi.com/locations/v2/search"

            querystring = {"query": self.user_data.get_city(), "locale": "ru_RU", "currency": "RUB"}

            headers = {
                "X-RapidAPI-Key": "a4a48b383fmsh7fc727029fd5ed8p19882cjsn51fd4f2b505e",
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            data = json.loads(response.text)

            with open(f'{message.from_user.id}', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

            with open(f'{message.from_user.id}', 'r', encoding='utf-8') as files:
                jse = json.load(files)
                for one in jse:
                    if one == 'suggestions':
                        for two in jse[one]:
                            for three in two['entities']:
                                b_say = three['name']

                                self.bot.send_message(message.from_user.id, b_say)
                                print(f'Бот ответил: {b_say}')
                                time.sleep(0.5)

        except (ValueError, AttributeError):
            print(self.info_highprice.__name__, 'Ошибка')
            self.bot.register_next_step_handler(message.from_user.id, self.getTextMessages)

    def Help(self, message):

        print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')

        markup = types.ReplyKeyboardMarkup()

        lowprice_button = types.KeyboardButton('/lowprice')
        highprice_button = types.KeyboardButton('/highprice')
        bestdeal_button = types.KeyboardButton('/bestdeal')
        history_button = types.KeyboardButton('/history_button')

        markup.add(lowprice_button, highprice_button, bestdeal_button, history_button)
        if message.text == "Привет":
            self.bot.send_message(message.from_user.id, config.b_say_help_commands)
        elif message.text == "/help":
            self.bot.send_message(message.from_user.id, "Команды", reply_markup=markup)
        else:
            self.bot.send_message(message.from_user.id, config.b_say_help)

    def getTextMessages(self, message):
        self.Help(message=message)


    def calendar(self, message):
        calendar, step = DetailedTelegramCalendar().build()
        self.bot.send_message(message.chat.id,
                         f"Выберите: {LSTEP[step]}",
                         reply_markup=calendar)

    def calendar2(self, message):
        calendar, step = DetailedTelegramCalendar().build()
        self.bot.send_message(message.chat.id,
                         f"Выберите: {LSTEP[step]}",
                         reply_markup=calendar)