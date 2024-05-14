import sqlite3

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS MenuItems
             (id INTEGER PRIMARY KEY, name TEXT, price REAL, type TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Orders
             (id INTEGER PRIMARY KEY, table_number INTEGER, order_type TEXT, status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS OrderItems
             (id INTEGER PRIMARY KEY, order_id INTEGER, item_id INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations
                        (id INTEGER PRIMARY KEY, table_number INTEGER, reservation_time TEXT, party_size INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Payments
             (id INTEGER PRIMARY KEY, order_id INTEGER, amount REAL, payment_method TEXT)''')

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_reservation(self, table_number, reservation_time, party_size):
        c.execute("INSERT INTO Reservations (table_number, reservation_time, party_size) VALUES (?, ?, ?)",
                       (table_number, reservation_time, party_size))
        conn.commit()
        return "Reservation created successfully"

    def assign_table(self):
        for table, status in self.tables.items():
            if not status:
                return table
        return None

    def add_menu_item(self, name, price, item_type):
        c.execute("INSERT INTO MenuItems (name, price, type) VALUES (?, ?, ?)", (name, price, item_type))
        conn.commit()

    def get_menu_items(self):
        c.execute("SELECT * FROM MenuItems")
        return c.fetchall()

    def add_user(self, username, password):
        c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

    def get_users(self):
        c.execute("SELECT * FROM Users")
        return c.fetchall()

    def add_payment(self, order_id, amount, payment_method):
        c.execute("INSERT INTO Payments (order_id, amount, payment_method) VALUES (?, ?, ?)",
                  (order_id, amount, payment_method))
        conn.commit()
    
    def get_reservations(self):
        c.execute("SELECT * FROM Reservations")
        reservations = c.fetchall()
        print("Reservations:", reservations)  # Add this line for debugging
        return reservations

# Close the database connection
conn.close()