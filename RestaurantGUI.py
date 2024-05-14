import tkinter as tk
from tkinter import messagebox

# import required class
from Restaurant import Restaurant
from Database import Database

# GUI
class RestaurantGUI:
    def __init__(self, master):
        self.master = master
        self.database = Database('restaurant.db')

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

        self.menu_items = self.database.get_menu_items()

        self.menu_item_label = tk.Label(master, text="Menu Items:")
        self.menu_item_label.pack()

        self.reservation_frame = tk.Frame(master)
        self.reservation_frame.pack()

        self.view_reservations_button = tk.Button(master, text="View Reservations", command=self.view_reservations)
        self.view_reservations_button.pack()

        for item in self.menu_items:
            tk.Label(master, text=item[1] + " - $" + str(item[2])).pack()
    
    def run(self):
        self.master.mainloop()

    def create_order(self):
        table_number = Database.assign_table()
        if table_number:
            order = Restaurant.create_order(table_number, "Dine-in")
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
        reservations = Database.get_reservations()
        if reservations:
            reservation_window = tk.Toplevel(self.master)
            reservation_window.title("Reservations")

            for i, reservation in enumerate(reservations, start=1):
                reservation_info = f"Reservation {i}:\nTable Number: {reservation[1]}\nReservation Time: {reservation[2]}\nParty Size: {reservation[3]}\n\n"
                tk.Label(reservation_window, text=reservation_info).pack()
        else:
            messagebox.showinfo("No Reservations", "There are no reservations.")

    def submit_reservation(self, window, table_number, reservation_time, party_size):
        Database.create_reservation(table_number, reservation_time, party_size)
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
        Database.add_menu_item(name, float(price), item_type)
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
        Database.add_user(username, password)
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
        Database.add_payment(int(order_id), float(amount), method)
        messagebox.showinfo("Payment Added", "Payment added successfully!")
        window.destroy()