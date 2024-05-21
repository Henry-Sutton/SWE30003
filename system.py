import sqlite3
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

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

        self.label = ttk.Label(master, text="Welcome to Relaxing Koala Restaurant!")
        self.label.grid(row=0, column=0, columnspan=3) #6 x 4

        #self.table_frame = tk.Frame(master)
        #self.table_frame.pack()

        self.create_order_button = ttk.Button(master, text="Create Order", command=self.open_create_order_window)
        self.create_order_button.grid(row=1, column=0)

        self.view_order_button = ttk.Button(master, text="View Order", command=self.open_view_order_window)
        self.view_order_button.grid(row=2, column=0)

        self.create_reservation_button = ttk.Button(master, text="Create Reservation", command=self.create_reservation)
        self.create_reservation_button.grid(row=6, column=3)

        self.menu_items = restaurant.get_menu_items()

        self.update_reservations()

    def update_reservations(self):
        self.reservations_list = tk.Listbox(self.master)
        self.reservations_list.grid(row=1, column=3, rowspan=5)

        self.reservation_scrollbar = tk.Scrollbar(self.master)
        reservations = restaurant.get_reservations()

        for r in reservations:
            self.reservations_list.insert("end", r)

        self.reservations_list.config(yscrollcommand = self.reservation_scrollbar.set) 

    def open_create_order_window(self):
        create_order_window = tk.Toplevel(self.master)
        create_order_window.title("Create Order")
        create_order_window.geometry("400x400")

        selected_items = []

        for item in self.menu_items:
            Btn = ttk.Button(create_order_window, text=item[1], command=lambda: self.add_item_to_order(create_order_window, item[1]))
            Btn.pack(pady=10)

        submit_button = ttk.Button(create_order_window, text="Submit", command=lambda: self.submit_order(selected_items, create_order_window))
        submit_button.pack()

    def submit_order(self, selected_items, window):
        selected_items = [item[1] for item in selected_items if item[0].get()]
        if selected_items:
            # Assuming table number and order type are selected elsewhere
            table_number = 1  # Example table number
            order_type = "Dine-in"  # Example order type
            order = restaurant.create_order(table_number, order_type)
            for item in selected_items:
                order.add_item(MenuItem(item[1], item[2], item[3]))
            messagebox.showinfo("Order Created", f"Order created for Table {table_number}")
            window.destroy()
        else:
            messagebox.showwarning("No Items Selected", "Please select at least one item.")

    def open_view_order_window(self):
        view_order_window = tk.Toplevel(self.master)
        view_order_window.title("View Orders")

        orders = restaurant.orders
        if orders:
            for i, order in enumerate(orders, start=1):
                ttk.Button(view_order_window, text=f"Order {i}", command=lambda order=order: self.open_order_details_window(order)).pack()
        else:
            tk.Label(view_order_window, text="No orders available.").pack()

    def open_order_details_window(self, order):
        order_details_window = tk.Toplevel(self.master)
        order_details_window.title("Order Details")

        tk.Label(order_details_window, text=f"Table Number: {order.table_number}").pack()
        tk.Label(order_details_window, text=f"Order Type: {order.order_type}").pack()
        tk.Label(order_details_window, text="Items:").pack()
        for item in order.items:
            tk.Label(order_details_window, text=f"{item.name} - ${item.price}").pack()
        ttk.Button(order_details_window, text="Pay", command=lambda: self.pay_order(order)).pack()

    def pay_order(self, order):
        # Your payment logic here
        messagebox.showinfo("Payment", "Payment for order successfully processed.")


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
        self.update_reservations()
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
    root = ttk.window.Window(size=[640, 480])
    app = RestaurantApp(root)
    root.mainloop()

if __name__ == "__main__":
    restaurant = Restaurant()
    main()

# Close the database connection
conn.close()
