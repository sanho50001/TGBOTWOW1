import telebot
import datetime
from dotenv import load_dotenv
import os
from BOT.commands import main


# Загрузка среды окружения
load_dotenv()

# Запуск бота по токену
bot = telebot.TeleBot(token=os.getenv('token'))

# Отпределение команд бота
TGBOT = main.CommandsTelegram(bot)

print('Бот начал свою работу.')

# Хандлеры для вызова команд

# Хендлер для регистрации
@bot.message_handler(commands=["reg"])
def reg(message):
    # print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')

    bot.send_message(message.from_user.id, 'Начинаем процесс регистрации...')


@bot.message_handler(commands=['setting'])
def setting(message):
    if message.from_user.last_name or message.from_user.first_name == 'Shuero':
        bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.last_name or message.from_user.first_name}')
        TGBOT.set_admin_setting(message)

# Хендлер старта
@bot.message_handler(commands=['start'])
def start(message):
    print(f'Чат ID: {message.chat.id} | {message.from_user.first_name} {message.from_user.last_name}: {message.text}')
    bot.send_message(message.from_user.id, 'text')

# хендлер принимающий любой вид текста которые не прошли проверку на команду
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    TGBOT.getTextMessages(message=message)

# Вечный пуллинг, чтобы бот принимал всегда сообщения
bot.polling(none_stop=True, interval=0)
print(f'Бот завершил работу в', datetime.datetime.now().strftime('Дата: %Y %m %d Время: %H:%M:%S'))

