import telebot
import datetime
import time
import config
import combot


bot = telebot.TeleBot(token=config.TGBot_token)

TGBOT = combot.CommandsTelegram(bot)

@bot.message_handler(commands=["lowprice"])
def lowprice(message):
    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    bot.send_message(message.from_user.id, config.b_ask_city)
    print(f'Ответ бота: {config.b_ask_city}')
    print()
    bot.register_next_step_handler(message, TGBOT.set_city)

@bot.message_handler(commands=["highprice"])
def highprice(message):

    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    bot.send_message(message.from_user.id, config.b_ask_city)

    print(f'Ответ бота: {config.b_ask_city}')
    print()

    bot.register_next_step_handler(message, TGBOT.set_city)


@bot.message_handler(commands=["bestdeal"])
def bestdeal(message):

    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    bot.send_message(message.from_user.id, config.b_ask_city)
    print(f'Ответ бота: {config.b_ask_city}')
    print()

    bot.register_next_step_handler(message, TGBOT.set_city)


@bot.message_handler(commands=["history"])
def history(message):
    bot.send_message(message.from_user.id, TGBOT.user_data.get_year())
    bot.send_message(message.from_user.id, TGBOT.user_data.get_month())
    bot.send_message(message.from_user.id, TGBOT.user_data.get_day())


    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    #
    # bot.send_message(message.from_user.id, config.b_say_start_history)
    # print(f'Ответ бота: {config.b_say_start_history}')
    # print()
    #
    # bot.register_next_step_handler(message, TGBOT.set_city)


@bot.message_handler(commands=['calendar'])
def start_calendar(message):
    combot.CommandsTelegram.calendar(TGBOT, message)



@bot.callback_query_handler(func=combot.DetailedTelegramCalendar.func())
def cal(calendar):
    today_date = datetime.date.today()
    result, key, step = combot.DetailedTelegramCalendar(min_date=today_date, locale='ru').process(calendar.data)
    if not result and key:
        bot.edit_message_text(f"Выберите: {combot.LSTEP[step]}",
                              calendar.message.chat.id,
                              calendar.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали: {result}",
                              calendar.message.chat.id,
                              calendar.message.message_id)
        data = []
        i_date = []
        for i in calendar.data.split('_'):
            data.append(i)
        for i_data in data:
            i_date.append(i_data)
        del i_date[0:4]
        print(i_date)

        year = i_date[0]
        mouth = i_date[1]
        day = i_date[2]
        TGBOT.user_data.set_datetime_in(day, mouth, year)
        # print(year, mouth, day)


@bot.callback_query_handler(func=combot.DetailedTelegramCalendar.func())
def cal2(calendar):
    today_date = datetime.date.today()
    result, key, step = combot.DetailedTelegramCalendar(min_date=today_date, locale='ru').process(calendar.data)
    if not result and key:
        bot.edit_message_text(f"Выберите: {combot.LSTEP[step]}",
                              calendar.message.chat.id,
                              calendar.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали: {result}",
                              calendar.message.chat.id,
                              calendar.message.message_id)
        data = []
        i_date = []
        for i in calendar.data.split('_'):
            data.append(i)
        for i_data in data:
            i_date.append(i_data)
        del i_date[0:4]
        print(i_date)

        year = i_date[0]
        mouth = i_date[1]
        day = i_date[2]
        TGBOT.user_data.set_datetime_out(day, mouth, year)

@bot.message_handler(commands=['start'])
def start(message):
    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    bot.send_message(message.from_user.id, config.b_start_say)




@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    TGBOT.getTextMessages(message=message)


bot.polling(none_stop=True, interval=0)
print(f'Бот завершил работу в', datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S'))



