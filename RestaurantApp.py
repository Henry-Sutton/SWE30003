import tkinter as tk
import ttkbootstrap as ttk

from MenuItem import MenuItem
from Restaurant import Restaurant
from Order import Order

class RestaurantApp:
    def __init__(self, master, restaurant):
        self.master = master
        self.restaurant = restaurant
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

        self.menu_items = self.restaurant.get_menu_items()

        self.update_reservations()

    def update_reservations(self):
        self.reservations_list = tk.Listbox(self.master)
        self.reservations_list.grid(row=1, column=3, rowspan=5)

        self.reservation_scrollbar = tk.Scrollbar(self.master)
        reservations = self.restaurant.get_reservations()

        for r in reservations:
            self.reservations_list.insert("end", r)

        self.reservations_list.config(yscrollcommand = self.reservation_scrollbar.set) 

    def open_create_order_window(self):
        create_order_window = tk.Toplevel(self.master)
        create_order_window.title("Create Order")
        create_order_window.geometry("400x400")

        label = ttk.Label(create_order_window, text="Table Number")
        label.pack()
        table_number = tk.IntVar()
        optionMenu = ttk.OptionMenu(create_order_window, table_number, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        optionMenu.pack()

        selected_items = []

        for item in self.menu_items:
            Btn = ttk.Button(create_order_window, text=item[1], command=lambda item=item: selected_items.append(item))
            Btn.pack(pady=10)

        submit_button = ttk.Button(create_order_window, text="Submit", command=lambda: self.submit_order(table_number.get(), selected_items))
        submit_button.pack()

    def submit_order(self, table_number, selected_items):
        order = self.restaurant.create_order(table_number, selected_items)
        print(order.table_number, order.total, order.items)
        tk.messagebox.showinfo("Order Created", f"Order created for Table {table_number}, for ${order.total}")
            

    def open_view_order_window(self):
        view_order_window = tk.Toplevel(self.master)
        view_order_window.title("View Orders")

        orders = self.restaurant.orders
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
        tk.messagebox.showinfo("Payment", "Payment for order successfully processed.")


    def create_order(self):
        table_number = self.restaurant.assign_table()
        if table_number:
            order = self.restaurant.create_order(table_number, "Dine-in")
            tk.messagebox.showinfo("Order Created", f"Order created for Table {table_number}")
        else:
            tk.messagebox.showwarning("No Available Tables", "No available tables at the moment.")

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
        reservations = self.restaurant.get_reservations()
        if reservations:
            reservation_window = tk.Toplevel(self.master)
            reservation_window.title("Reservations")

            for i, reservation in enumerate(reservations, start=1):
                reservation_info = f"Reservation {i}:\nTable Number: {reservation[1]}\nReservation Time: {reservation[2]}\nParty Size: {reservation[3]}\n\n"
                tk.Label(reservation_window, text=reservation_info).pack()
        else:
            tk.messagebox.showinfo("No Reservations", "There are no reservations.")

    def submit_reservation(self, window, table_number, reservation_time, party_size):
        self.restaurant.create_reservation(int(table_number), reservation_time, int(party_size))
        tk.messagebox.showinfo("Reservation Created", "Reservation created successfully!")
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
        self.restaurant.add_menu_item(name, float(price), item_type)
        tk.messagebox.showinfo("Menu Item Added", "Menu item added successfully!")
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
        self.restaurant.add_user(username, password)
        tk.messagebox.showinfo("User Added", "User added successfully!")
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
        self.restaurant.add_payment(int(order_id), float(amount), method)
        tk.messagebox.showinfo("Payment Added", "Payment added successfully!")
        window.destroy()