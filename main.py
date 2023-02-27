# Импортируем функцию для создания объекта бота
from telebot import TeleBot
# Импортируем основные настройки проекта
from settings import config
# Импортируем главный класс-обработчик бота
from handlers.handler_main import HandlerMain


class Telegrambot:
    """
    Основной класс телеграмм бота (сервер), в основе которого
    используется библиотека pyTelegrambotAPI
    """
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        """
        Инициализация бота
        """
        # получаем токен
        self.token = config.TOKEN
        # инициализируем бот на основе зарегистрированного токена
        self.bot = TeleBot(self.token)
        # инициазиируем обработчик событий
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод предназначен для старта обработчика событий
        """
        self.handler.handle()

    def run_bot(self):
        # обработчик событий
        self.start()
        # служит для запуска бота
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = Telegrambot()
    bot.run_bot()

