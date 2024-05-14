class Order:
    def __init__(self, table_number, order_type):
        self.table_number = table_number
        self.order_type = order_type
        self.status = 'Pending'
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item.price for item in self.items)