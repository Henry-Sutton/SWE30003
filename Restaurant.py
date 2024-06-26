from MenuItem import MenuItem
from Order import Order
from Reservation import Reservation
from User import User
from Payment import Payment
from Cash import Cash
from Card import Card

class Restaurant:
    def __init__(self, c, conn):
        self.tables = {1: None, 2: None, 3: None}  # Example tables
        self.orders = []
        self.c = c 
        self.conn = conn

    def create_order(self, table_number, order_type, selected_items):
        order = Order(table_number, order_type, selected_items)
        self.orders.append(order)
        return order

    def create_reservation(self, table_number, reservation_time, party_size,name):
        self.c.execute("INSERT INTO Reservations (table_number, reservation_time, party_size,name) VALUES (?, ?, ?,?)",
                       (table_number, reservation_time, party_size,name))
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

    def add_payment(self, order, amount, payment_method):
        order_id = self.orders.index(order)
        self.c.execute("INSERT INTO Payments (order_id, amount, payment_method) VALUES (?, ?, ?)",
                  (order_id, amount, payment_method))
        self.conn.commit()
        if (payment_method == "cash"):
            method = Cash(amount)
        else:
            method = Card(amount)
        self.orders.pop(order_id)
        return Payment(order_id, method)
    
    def get_reservations(self):
        self.c.execute("SELECT * FROM Reservations")
        reservations = self.c.fetchall()
        #print("Reservations:", reservations)  # Add this line for debugging
        return reservations