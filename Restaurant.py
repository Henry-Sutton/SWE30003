import Order


class Restaurant:
    def __init__(self, c, conn):
        self.tables = {1: None, 2: None, 3: None}  # Example tables
        self.orders = []
        self.c = c 
        self.conn = conn

    def create_order(self, table_number, order_type):
        order = Order(table_number, order_type)
        self.orders.append(order)
        return order

    def create_reservation(self, table_number, reservation_time, party_size):
        self.c.execute("INSERT INTO Reservations (table_number, reservation_time, party_size) VALUES (?, ?, ?)",
                       (table_number, reservation_time, party_size))
        self.conn.commit()
        return "Reservation created successfully"

    def assign_table(self):
        for table, status in self.tables.items():
            if not status:
                return table
        return None

    def add_menu_item(self, name, price, item_type):
        self.c.execute("INSERT INTO MenuItems (name, price, type) VALUES (?, ?, ?)", (name, price, item_type))
        self.conn.commit()

    def get_menu_items(self):
        self.c.execute("SELECT * FROM MenuItems")
        return self.c.fetchall()

    def add_user(self, username, password):
        self.c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def get_users(self):
        self.c.execute("SELECT * FROM Users")
        return self.c.fetchall()

    def add_payment(self, order_id, amount, payment_method):
        self.c.execute("INSERT INTO Payments (order_id, amount, payment_method) VALUES (?, ?, ?)",
                  (order_id, amount, payment_method))
        self.conn.commit()
    
    def get_reservations(self):
        self.c.execute("SELECT * FROM Reservations")
        reservations = self.c.fetchall()
        print("Reservations:", reservations)  # Add this line for debugging
        return reservations