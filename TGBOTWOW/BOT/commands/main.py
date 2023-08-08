from BOT.main import user
from telebot import types
from .register import register
from .settings import Settings


# Класс команд телеграмма.
class CommandsTelegram:

    def __init__(self, bot):
        self.bot = bot
        self.user_data = user.User()
        self.setting = Settings()

    def Help(self, message):
        # вызов метода создания кнопки
        markup_reply = types.ReplyKeyboardMarkup()
        markup_inline = types.InlineKeyboardMarkup()

        # кнопки
        reg_button = types.KeyboardButton('/reg')

        # создание кнопки и добавление туда кнопок.
        markup_reply.add(reg_button)
        markup_inline.add(
            types.InlineKeyboardButton(text='register', callback_data='register')
        )

        if message.text == "text":
            self.bot.send_message(message.from_user.id, 'text')
        elif message.text == "/help":
            self.bot.send_message(message.from_user.id, "Команды", reply_markup=markup_reply)
        else:
            self.bot.send_message(message.from_user.id, 'Извините, я вас не совсем понимаю.')

    # Обработчик сообщений. Срабатывает когда сообщение не прошло проверку на команду
    def getTextMessages(self, message):
        self.Help(message=message)

    def reg(self, message):
        register(url=self.setting.get_connect(), user_id=message.from_user.id)

    def set_admin_setting(self, message):
        self.bot.send_message(message.from_user.id, 'Изменение настроек. Введите сайт регистрации')
        self.bot.register_next_step_handler(message, self.set_connect_url)

    def set_connect_url(self, message):
        self.setting.set_connect(message.text)
        self.bot.send_message(message.from_user.id, 'Изменен сайт регистрации')