# Импортируем класс родитель
from handlers.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.д
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        Обрабатывает входящие /start команды
        """

        self.bot.send_message(message.chat.id,
                              f'{message.from_user.first_name},'
                              f'Здравствуйте! Жду дальнейших указаний.',
                              reply_markup=self.keyboards.start_menu())

    def handle(self):
        # обработчик(декоратор) сообщений который обрататывает /start команды
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
