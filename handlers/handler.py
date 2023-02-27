# Импортируем библиотеку abc для реализации абстрактных классов
import abc
# Импортируем роазметку клавиатуры и клавиш
from markup.markup import Keyboards
# Импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager



class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keyboards = Keyboards()
        # инициализируем менеджер для работы с БД
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
