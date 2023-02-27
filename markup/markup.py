# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
# импортируем настройки и утилиты
from settings import config
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboads предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        Создаем и возвращаем кнопку по входным параметрам
        """

        if name == 'AMOUNT_ORDERS':
            config.KEYBOARD['AMOUNT_ORDERS'] = '{} {} {}'.format(step + 1, ' из ', str(
                self.DB.count_rows_order()))

        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD['AMOUNT_PRODUCT'] = '{}'.format(quantity)

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создаем разметку кнопок в основном меню и возвращаем разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn_1 = self.set_btn('CHOOSE_GOODS')
        item_btn_2 = self.set_btn('INFO')
        item_btn_3 = self.set_btn('SETTINGS')
        # расположение кнопок в меню
        self.markup.row(item_btn_1)
        self.markup.row(item_btn_2, item_btn_3)
        return self.markup

    def info_menu(self):
        """
        Создаем разметку кнопок в меню info
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn_1 = self.set_btn('<<')
        # расположение кнопок в меню
        self.markup.row(item_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создаем разметку кнопок в меню settings
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn_1 = self.set_btn('<<')
        # расположение кнопок
        self.markup.row(item_btn_1)
        return self.markup

    def remove_menu(self):
        """
        Удаляет данные кнопки и возвращает ее
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создаем разметку кнопок в меню категорий товара и возвращаем ее
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает и возвращает инлайн-кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создает разметку инлайн-кнопок в выбранной
        категории товара и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в названия инлайн-кнопок данные
        # из БД в соответствие с категорией товара
        for itm in self.DB.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(itm))

        return self.markup

    def orders_menu(self, step, quantity):
        """
        Создает разметки кнопок в заказе товара и возвращает разметки
        """

        self.markup = ReplyKeyboardMarkup(True, True)
        item_btn_1 = self.set_btn('X', step, quantity)
        item_btn_2 = self.set_btn('DOWN', step, quantity)
        item_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        item_btn_4 = self.set_btn('UP', step, quantity)

        item_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        item_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        item_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        item_btn_8 = self.set_btn('APPLAY', step, quantity)
        item_btn_9 = self.set_btn('<<', step, quantity)

        # расположение кнопок
        self.markup.row(item_btn_1, item_btn_2, item_btn_3, item_btn_4)
        self.markup.row(item_btn_5, item_btn_6, item_btn_7)
        self.markup.row(item_btn_9, item_btn_8)

        return self.markup
