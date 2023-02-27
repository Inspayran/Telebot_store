from handlers.handler import Handler
from settings import config, utility
from settings.message import MESSAGES


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_category(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку выбрать товар
        """
        self.bot.send_message(message.chat.id, 'Каталог категорий товара',
                              reply_markup=self.keyboards.remove_menu())

        self.bot.send_message(message.chat.id, 'Сделайте свой выбор',
                              reply_markup=self.keyboards.category_menu())

    def pressed_btn_info(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку TradingStore.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку settings.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обрабатывает входяие текстовые сообщения от нажатия на кнопку back.
        """
        self.bot.send_message(message.chat.id, 'Вы вернулись назад',
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_product(self, message, product):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопки категорий товаров
        """
        self.bot.send_message(message.chat.id, 'Категория ' + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))

        self.bot.send_message(message.chat.id, 'Ок',
                              reply_markup=self.keyboards.category_menu())

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователя при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step+1), parse_mode='HTML')
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(
                                  self.DB.select_single_product_name(product_id),
                                  self.DB.select_single_product_title(product_id),
                                  self.DB.select_single_product_price(product_id),
                                  self.DB.select_order_quantity(product_id)),
                              parse_mode='HTML', reply_markup=self.keyboards.orders_menu(
                                self.step, quantity))

    def pressed_btn_order(self, message):
        """
        Обрабатывает входяие текстовые сообщения от нажатия на кнопки "Заказ".
        """
        # Обнуляем данные шага
        self.step = 0
        # Получаем список всех продуктов в заказе
        count = self.DB.select_all_product_id()
        # Получаем количество по каждой позиции товара в заказе
        quantity = self.DB.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_up(self, message):
        """
        Обрабатывает входящие текстовые соббщения от нажатия на кнпоку up
        """
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем кол-во конкретной позиции заказов
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # получаем кол-во конкретной позиции продуктов
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД orders
            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            #вносим изменения в БД products
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        """
        Обрабатывает входящие текстовые соббщения от нажатия на кнпоку down
        """
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем кол-во конкретной позиции заказов
        quantity_order = self.DB.select_order_quantity(count[self.step])
        # получаем кол-во конкретной позиции продуктов
        quantity_product = self.DB.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД orders
            self.DB.update_order_value(count[self.step], 'quantity', quantity_order)
            #вносим изменения в БД products
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1
        count = self.DB.select_all_product_id()
        quantity = self.DB.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        if self.step < self.DB.count_rows_order()-1:
            self.step += 1
        count = self.DB.select_all_product_id()
        quantity = self.DB.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_x(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку х удалить позицию шага
        """
        # получаем список всех product_id заказа
        count = self.DB.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            # получаем кол-во конкретной позиции в заказе
            quantity_order = self.DB.select_order_quantity(count[self.step])
            # получаем кол-во товара к конкретной позиции заказа для возврата в product
            quantity_product = self.DB.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.DB.delete_order(count[self.step])
            # вносим изменения в БД product
            self.DB.update_product_value(count[self.step], 'quantity', quantity_product)
            # уменьшаем шаг
            self.step -=1

        count = self.DB.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:

            quantity_order = self.DB.select_order_quantity(count[self.step])
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'], parse_mode='HTML',
                                  reply_markup=self.keyboards.category_menu())

    def pressed_btn_applay(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на "оформить заказ"
        """
        # отправляем ответ пользователю
        self.bot.send_message(message.chat.id, MESSAGES['applay'].format(
            utility.get_total_cost(self.DB),
            utility.get_total_quantity(self.DB)),
                              parse_mode='html',
        reply_markup=self.keyboards.category_menu())
        # очищаем данные с заказа
        self.DB.delete_all_order()


    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** Меню ********** #

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            # ********** Меню категории товара ********** #
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.DB.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keyboards.category_menu())

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_applay(message)

