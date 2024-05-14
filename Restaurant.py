from Order import Order

class Restaurant:
    def __init__(self):
        self.tables = {1: None, 2: None, 3: None}  # Example tables
        self.orders = []

    def create_order(self, table_number, order_type):
        order = Order(table_number, order_type)
        self.orders.append(order)
        return order

