import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database Initialization
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

# Classes
class MenuItem:
    def __init__(self, name, price, item_type):
        self.name = name
        self.price = price
        self.type = item_type

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

class Reservation:
    def __init__(self, table_number, reservation_time, party_size):
        self.table_number = table_number
        self.reservation_time = reservation_time
        self.party_size = party_size

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Payment:
    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method

class Restaurant:
    def __init__(self):
        self.tables = {1: None, 2: None, 3: None}  # Example tables
        self.orders = []

    def create_order(self, table_number, order_type):
        order = Order(table_number, order_type)
        self.orders.append(order)
        return order

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

# GUI
class RestaurantApp:
    def __init__(self, master):
        self.master = master
        master.title("Restaurant Management System")

        self.label = tk.Label(master, text="Welcome to Relaxing Koala Restaurant!")
        self.label.pack()

        self.table_frame = tk.Frame(master)
        self.table_frame.pack()

        self.create_order_button = tk.Button(master, text="Create Order", command=self.create_order)
        self.create_order_button.pack()

        self.create_reservation_button = tk.Button(master, text="Create Reservation", command=self.create_reservation)
        self.create_reservation_button.pack()

        self.add_item_button = tk.Button(master, text="Add Menu Item", command=self.add_menu_item)
        self.add_item_button.pack()

        self.add_user_button = tk.Button(master, text="Add User", command=self.add_user)
        self.add_user_button.pack()

        self.add_payment_button = tk.Button(master, text="Add Payment", command=self.add_payment)
        self.add_payment_button.pack()

        self.menu_items = restaurant.get_menu_items()

        self.menu_item_label = tk.Label(master, text="Menu Items:")
        self.menu_item_label.pack()

        self.reservation_frame = tk.Frame(master)
        self.reservation_frame.pack()

        self.view_reservations_button = tk.Button(master, text="View Reservations", command=self.view_reservations)
        self.view_reservations_button.pack()

        for item in self.menu_items:
            tk.Label(master, text=item[1] + " - $" + str(item[2])).pack()

    def create_order(self):
        table_number = restaurant.assign_table()
        if table_number:
            order = restaurant.create_order(table_number, "Dine-in")
            messagebox.showinfo("Order Created", f"Order created for Table {table_number}")
        else:
            messagebox.showwarning("No Available Tables", "No available tables at the moment.")

    def create_reservation(self):
        reservation_window = tk.Toplevel(self.master)
        reservation_window.title("Create Reservation")

        table_label = tk.Label(reservation_window, text="Table Number:")
        table_label.grid(row=0, column=0)
        table_entry = tk.Entry(reservation_window)
        table_entry.grid(row=0, column=1)

        time_label = tk.Label(reservation_window, text="Reservation Time:")
        time_label.grid(row=1, column=0)
        time_entry = tk.Entry(reservation_window)
        time_entry.grid(row=1, column=1)

        party_size_label = tk.Label(reservation_window, text="Party Size:")
        party_size_label.grid(row=2, column=0)
        party_size_entry = tk.Entry(reservation_window)
        party_size_entry.grid(row=2, column=1)

        submit_button = tk.Button(reservation_window, text="Submit",
                                  command=lambda: self.submit_reservation(reservation_window, table_entry.get(),
                                                                          time_entry.get(), party_size_entry.get()))
        submit_button.grid(row=3, columnspan=2)

    def view_reservations(self):
        reservations = restaurant.get_reservations()
        if reservations:
            reservation_window = tk.Toplevel(self.master)
            reservation_window.title("Reservations")

            for i, reservation in enumerate(reservations, start=1):
                reservation_info = f"Reservation {i}:\nTable Number: {reservation[1]}\nReservation Time: {reservation[2]}\nParty Size: {reservation[3]}\n\n"
                tk.Label(reservation_window, text=reservation_info).pack()
        else:
            messagebox.showinfo("No Reservations", "There are no reservations.")

    def submit_reservation(self, window, table_number, reservation_time, party_size):
        restaurant.create_reservation(int(table_number), reservation_time, int(party_size))
        messagebox.showinfo("Reservation Created", "Reservation created successfully!")
        window.destroy()

    def add_menu_item(self):
        add_item_window = tk.Toplevel(self.master)
        add_item_window.title("Add Menu Item")

        name_label = tk.Label(add_item_window, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(add_item_window)
        name_entry.grid(row=0, column=1)

        price_label = tk.Label(add_item_window, text="Price:")
        price_label.grid(row=1, column=0)
        price_entry = tk.Entry(add_item_window)
        price_entry.grid(row=1, column=1)

        type_label = tk.Label(add_item_window, text="Type:")
        type_label.grid(row=2, column=0)
        type_entry = tk.Entry(add_item_window)
        type_entry.grid(row=2, column=1)

        submit_button = tk.Button(add_item_window, text="Submit",
                                  command=lambda: self.submit_menu_item(add_item_window, name_entry.get(),
                                                                       price_entry.get(), type_entry.get()))
        submit_button.grid(row=3, columnspan=2)

    def submit_menu_item(self, window, name, price, item_type):
        restaurant.add_menu_item(name, float(price), item_type)
        messagebox.showinfo("Menu Item Added", "Menu item added successfully!")
        window.destroy()

    def add_user(self):
        add_user_window = tk.Toplevel(self.master)
        add_user_window.title("Add User")

        username_label = tk.Label(add_user_window, text="Username:")
        username_label.grid(row=0, column=0)
        username_entry = tk.Entry(add_user_window)
        username_entry.grid(row=0, column=1)

        password_label = tk.Label(add_user_window, text="Password:")
        password_label.grid(row=1, column=0)
        password_entry = tk.Entry(add_user_window)
        password_entry.grid(row=1, column=1)

        submit_button = tk.Button(add_user_window, text="Submit",
                                  command=lambda: self.submit_user(add_user_window, username_entry.get(),
                                                                   password_entry.get()))
        submit_button.grid(row=2, columnspan=2)

    def submit_user(self, window, username, password):
        restaurant.add_user(username, password)
        messagebox.showinfo("User Added", "User added successfully!")
        window.destroy()

    def add_payment(self):
        add_payment_window = tk.Toplevel(self.master)
        add_payment_window.title("Add Payment")

        order_id_label = tk.Label(add_payment_window, text="Order ID:")
        order_id_label.grid(row=0, column=0)
        order_id_entry = tk.Entry(add_payment_window)
        order_id_entry.grid(row=0, column=1)

        amount_label = tk.Label(add_payment_window, text="Amount:")
        amount_label.grid(row=1, column=0)
        amount_entry = tk.Entry(add_payment_window)
        amount_entry.grid(row=1, column=1)

        method_label = tk.Label(add_payment_window, text="Payment Method:")
        method_label.grid(row=2, column=0)
        method_entry = tk.Entry(add_payment_window)
        method_entry.grid(row=2, column=1)

        submit_button = tk.Button(add_payment_window, text="Submit",
                                  command=lambda: self.submit_payment(add_payment_window, order_id_entry.get(),
                                                                      amount_entry.get(), method_entry.get()))
        submit_button.grid(row=3, columnspan=2)

    def submit_payment(self, window, order_id, amount, method):
        restaurant.add_payment(int(order_id), float(amount), method)
        messagebox.showinfo("Payment Added", "Payment added successfully!")
        window.destroy()

def main():
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()

if __name__ == "__main__":
    restaurant = Restaurant()
    main()

# Close the database connection
conn.close()
