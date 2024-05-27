class Order:
    def __init__(self, ident, table_number, selected_items):
        self.id = ident
        self.table_number = table_number
        self.order_type = 'Dine-in'
        self.status = 'Pending'
        self.items = selected_items
        self.total = self.calculate_total()

    def add_item(self, item):
        self.items.append(item)

    def calculate_total(self):
        return sum(item[2] for item in self.items)