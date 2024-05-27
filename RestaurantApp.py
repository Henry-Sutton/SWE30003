import tkinter as tk
import ttkbootstrap as ttk
import Restaurant
import MenuItem

class RestaurantApp:
    def __init__(self, master, restaurant):
        self.master = master
        self.restaurant = restaurant
        master.title("Restaurant Management System")

        self.label = ttk.Label(master, text="Welcome to Relaxing Koala Restaurant!")
        self.label.grid(row=0, column=0, columnspan=4, padx=(10, 10), pady=(10, 10))  # Adjust columnspan as needed

        self.create_order_button = ttk.Button(master, text="Create Order", command=self.open_create_order_window)
        self.create_order_button.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

        self.view_order_button = ttk.Button(master, text="View Order", command=self.open_view_order_window)
        self.view_order_button.grid(row=2, column=0, padx=(10, 5), pady=(5, 5))

        self.create_reservation_button = ttk.Button(master, text="Create Reservation", command=self.create_reservation)
        self.create_reservation_button.grid(row=8, column=0, padx=(10, 5), pady=(5, 5))

        self.menu_items = self.restaurant.get_menu_items()

        # Set up the Treeview for reservations
        self.setup_reservation_treeview()

        # Fetch and display the initial reservations
        self.update_reservations()

    def setup_reservation_treeview(self):
        # Create a Treeview widget
        self.tree = ttk.Treeview(self.master, columns=("Reservation", "Table Number", "Reservation Time", "Party Size","Name"), show="headings")
        self.tree.grid(row=1, column=1, rowspan=7, columnspan=5, padx=(20, 10), pady=(10, 10), sticky='nsew')

        # Define the column headers
        self.tree.heading("Reservation", text="Reservation")
        self.tree.heading("Table Number", text="Table Number")
        self.tree.heading("Reservation Time", text="Reservation Time")
        self.tree.heading("Party Size", text="Party Size")
        self.tree.heading("Name", text="Name")

        # Define the column widths
        self.tree.column("Reservation", width=100)
        self.tree.column("Table Number", width=100)
        self.tree.column("Reservation Time", width=150)
        self.tree.column("Party Size", width=100)
        self.tree.column("Name", width = 100)

        # Add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=8, rowspan=7, sticky='ns', pady=(10, 10))

    def update_reservations(self):
        # Clear the current contents of the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and insert new reservations
        reservations = self.restaurant.get_reservations()
        for reservation in reservations:
            self.tree.insert("", "end", values=reservation)


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
            order = self.restaurant.create_order(table_number, order_type)
            for item in selected_items:
                order.add_item(MenuItem(item[1], item[2], item[3]))
            tk.messagebox.showinfo("Order Created", f"Order created for Table {table_number}")
            window.destroy()
        else:
            tk.messagebox.showwarning("No Items Selected", "Please select at least one item.")

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
        table_numbers = ["1", "2", "3", "4"]
        reservation_time = ["12:00", "12:30", "13:00", "13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00","17:30""18:00","18:30""19:00","19:30","20:00",
                            "20:30""21:00","21:30"]
        party_size = ["1","2","3","4","5","6","7","8","9+"]
        
        table_label = tk.Label(reservation_window, text="Table Number:")
        table_label.grid(row=0, column=0)
        table_entry = ttk.Combobox(reservation_window, values=table_numbers)
        table_entry.current(0)
        table_entry.grid(row=0, column=1)

        time_label = tk.Label(reservation_window, text="Reservation Time:")
        time_label.grid(row=1, column=0)
        time_entry = ttk.Combobox(reservation_window,values=reservation_time)
        table_entry.current(0)
        time_entry.grid(row=1, column=1)

        party_size_label = tk.Label(reservation_window, text="Party Size:")
        party_size_label.grid(row=2, column=0)
        party_size_entry = ttk.Combobox(reservation_window,values=party_size)
        table_entry.current(0)
        party_size_entry.grid(row=2, column=1)
        
        party_name_label = tk.Label(reservation_window, text="Name")
        party_name_label.grid(row=3, column=0)
        party_name_entry = tk.Entry(reservation_window)
        party_name_entry.grid(row=3, column=1)
        
        submit_button = tk.Button(reservation_window, text="Submit",
                                  command=lambda: self.submit_reservation(reservation_window, table_entry.get(),
                                                                          time_entry.get(), party_size_entry.get(),party_name_entry.get()))
        submit_button.grid(row=4, columnspan=2)

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

    def submit_reservation(self, window, table_number, reservation_time, party_size,name):
        self.restaurant.create_reservation(int(table_number), reservation_time, int(party_size),name)
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