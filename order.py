# order.py
class Order:
    def __init__(self):
        self.__order_list = []

    def add_item(self, item):
        self.__order_list.append(item)

    def remove_item(self, item):
        if item in self.__order_list:
            self.__order_list.remove(item)

    def get_order(self):
        return self.__order_list

    def total_cost(self, menu_data):
        total = 0
        for item in self.__order_list:
            if item in menu_data:
                total += menu_data[item]
        return total
