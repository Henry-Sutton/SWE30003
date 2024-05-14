import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        # Create tables if they don't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS MenuItems
                          (id INTEGER PRIMARY KEY, name TEXT, price REAL, type TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Orders
                          (id INTEGER PRIMARY KEY, table_number INTEGER, order_type TEXT, status TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS OrderItems
                          (id INTEGER PRIMARY KEY, order_id INTEGER, item_id INTEGER)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Reservations
                          (id INTEGER PRIMARY KEY, table_number INTEGER, reservation_time TEXT, party_size INTEGER)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Users
                          (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Payments
                          (id INTEGER PRIMARY KEY, order_id INTEGER, amount REAL, payment_method TEXT)''')

        self.conn.commit()

    def create_reservation(self, table_number, reservation_time, party_size):
        self.c.execute("INSERT INTO Reservations (table_number, reservation_time, party_size) VALUES (?, ?, ?)",
                        (table_number, reservation_time, party_size))
        self.conn.commit()
        return "Reservation created successfully"

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
        print("Reservations:", reservations)  # For debugging
        return reservations
