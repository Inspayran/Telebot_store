# конвертирует список с p[(5,),(8,),...] к [5,8,...]
def _convert(list_convert):

    return [itm[0] for itm in list_convert]


# считаем общую сумму заказа и возвращаем результат
def total_cost(list_quantity, list_price):

    order_total_cost = 0

    for index, item in enumerate(list_price):
        order_total_cost += list_quantity[index]*list_price[index]

        return order_total_cost


def total_quantity(list_quantity):

    order_total_quantity = 0
    for item in list_quantity:
        order_total_quantity += item

        return order_total_quantity


def get_total_cost(DB):
    """
    возвращает общую стоимость товара
    """
    # получаем список всех product_id заказа
    all_product_id = DB.select_all_product_id()
    # получаем список стоимости по всем позициям заказа в виде списка
    all_price = [DB.select_single_product_price(item) for item in all_product_id]
    # получаем список кол-ва по всем позициям заказа в виде списка
    all_quantity = [DB.select_order_quantity(item) for item in all_product_id]
    # вовзращаем общую стоимость
    return total_cost(all_quantity, all_price)


def get_total_quantity(DB):
    """
    Возвращает общее кол-во заказанной единицы набора
    """
    all_product_id = DB.select_all_product_id()
    # получаем список кол-ва по всем позициям заказа в виде обычного списка
    all_quantity = [DB.select_order_quantity(item) for item in all_product_id]
    return total_quantity(all_quantity)
