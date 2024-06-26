import tkinter as tk
import ttkbootstrap as ttk

from MenuItem import MenuItem
from Restaurant import Restaurant
from Order import Order

class RestaurantApp:
    def __init__(self, master, restaurant):
        self.master = master
        self.restaurant = restaurant
        master.minsize(800, 400)
        master.title("Restaurant Management System")

        self.label = ttk.Label(master, text="Welcome to Relaxing Koala Restaurant!")
        self.label.grid(row=0, column=0, columnspan=4, padx=(10, 10), pady=(10, 10))  # Adjust columnspan as needed

        self.create_order_button = ttk.Button(master, text="Create Order", command=self.open_create_order_window)
        self.create_order_button.grid(row=1, column=0, padx=(10, 5), pady=(5, 5))

        self.view_order_button = ttk.Button(master, text="View Orders", command=self.open_view_order_window)
        self.view_order_button.grid(row=2, column=0, padx=(10, 5), pady=(5, 5))

        self.add_menu_item_button = ttk.Button(master, text="Add Menu Item", command=self.add_menu_item)
        self.add_menu_item_button.grid(row=3, column=0, padx=(10, 5), pady=(5, 5))

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
        create_order_window.geometry("1100x600")

        # Table Number Label and OptionMenu
        label = ttk.Label(create_order_window, text="Table Number")
        label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        table_number = tk.IntVar(create_order_window, 1)
        optionMenu = tk.OptionMenu(create_order_window, table_number, *range(1, 16))
        optionMenu.grid(column=1, row=0, padx=5, pady=5, sticky='w')

        # Order type radio buttons
        order_type = tk.StringVar(create_order_window, value="Dine-in")
        dine_in_radiobutton = tk.Radiobutton(create_order_window, text="Dine-in", variable=order_type, value="Dine-in")
        takeaway_radiobutton = tk.Radiobutton(create_order_window, text="Takeaway", variable=order_type, value="Takeaway")
        delivery_radiobutton = tk.Radiobutton(create_order_window, text="Delivery", variable=order_type, value="Delivery")

        dine_in_radiobutton.grid(column=2, row=0, padx=5, pady=5, sticky='w')
        takeaway_radiobutton.grid(column=3, row=0, padx=5, pady=5, sticky='w')
        delivery_radiobutton.grid(column=4, row=0, padx=5, pady=5, sticky='w')

        # Text box for notes
        notes_label = ttk.Label(create_order_window, text="Notes")
        notes_label.grid(column=0, row=1, padx=5, pady=5, sticky='w')
        notes = tk.StringVar(create_order_window, "")
        noteBox = ttk.Entry(create_order_window, textvariable=notes)
        noteBox.grid(column=1, row=1, padx=5, pady=5, sticky='w')

        # Frame to hold the selected items list
        selected_frame = ttk.Frame(create_order_window)
        selected_frame.grid(column=0, row=2, rowspan=3, padx=5, pady=5, sticky='nw')

        selected_items = []

        selected_label = ttk.Label(selected_frame, text="Selected Items")
        selected_label.pack(anchor='w')

        selected_listbox = tk.Listbox(selected_frame, width=30)
        selected_listbox.pack(anchor='w', fill=tk.BOTH, expand=True)

        # Function to add selected item to the listbox
        def add_item(item):
            note = notes.get()
            selected_items.append((item, note))
            selected_listbox.insert(tk.END, item[1])
            if note:
                selected_listbox.insert(tk.END, f"  ** {note}")
            notes.set("")

        # Buttons for menu items in a 3x2 grid
        menu_frame = ttk.Frame(create_order_window)
        menu_frame.grid(column=1, row=2, rowspan=3, padx=5, pady=5, sticky='nw')

        for i, item in enumerate(self.menu_items):
            Btn = ttk.Button(menu_frame, text=item[1], command=lambda item=item: add_item(item))
            Btn.grid(column=i % 3, row=i // 3, padx=5, pady=5, sticky='w')

        # Submit button
        submit_button = ttk.Button(create_order_window, text="Submit", command=lambda: self.submit_order(order_type.get(), table_number.get(), selected_items, create_order_window))
        submit_button.grid(column=0, row=5, columnspan=5, padx=5, pady=5)

    def submit_order(self, order_type, table_number, selected_items, window):
        if order_type == "Dine-in":
            order = self.restaurant.create_order(table_number, "dine-in", selected_items)
            tk.messagebox.showinfo("Order Created", f"Dine-in order created for Table {table_number}, for ${order.total}")
            window.destroy()
        elif order_type == "Takeaway":
            self.open_takeaway_window(table_number, selected_items, window)
        elif order_type == "Delivery":
            self.open_delivery_window(table_number, selected_items, window)
            

    def open_view_order_window(self):
        view_order_window = tk.Toplevel(self.master)
        view_order_window.title("View Orders")

        orders = self.restaurant.orders
        if orders:
            for i, order in enumerate(orders, start=1):
                ttk.Button(view_order_window, text=f"Order {i}", command=lambda order=order: self.open_order_details_window(order)).pack()
        else:
            tk.Label(view_order_window, text="No orders available.").pack()

    def open_takeaway_window(self, table_number, selected_items, parent_window):
        takeaway_window = tk.Toplevel(parent_window)
        takeaway_window.title("Takeaway Order")
        takeaway_window.geometry("400x200")

        name_label = ttk.Label(takeaway_window, text="Customer Name")
        name_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        customer_name = tk.StringVar(takeaway_window, "")
        name_entry = ttk.Entry(takeaway_window, textvariable=customer_name)
        name_entry.grid(column=1, row=0, padx=5, pady=5, sticky='w')

        # Pay button
        pay_button = ttk.Button(takeaway_window, text="Pay", command=lambda: self.submit_order_takeaway(customer_name.get(), selected_items, takeaway_window, parent_window))
        pay_button.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

    def open_delivery_window(self, table_number, selected_items, parent_window):
        delivery_window = tk.Toplevel(parent_window)
        delivery_window.title("Delivery Order")
        delivery_window.geometry("400x300")

        name_label = ttk.Label(delivery_window, text="Customer Name")
        name_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')
        customer_name = tk.StringVar(delivery_window, "")
        name_entry = ttk.Entry(delivery_window, textvariable=customer_name)
        name_entry.grid(column=1, row=0, padx=5, pady=5, sticky='w')

        phone_label = ttk.Label(delivery_window, text="Phone Number")
        phone_label.grid(column=0, row=1, padx=5, pady=5, sticky='w')
        phone_number = tk.StringVar(delivery_window, "")
        phone_entry = ttk.Entry(delivery_window, textvariable=phone_number)
        phone_entry.grid(column=1, row=1, padx=5, pady=5, sticky='w')

        address_label = ttk.Label(delivery_window, text="Delivery Address")
        address_label.grid(column=0, row=2, padx=5, pady=5, sticky='w')
        delivery_address = tk.StringVar(delivery_window, "")
        address_entry = ttk.Entry(delivery_window, textvariable=delivery_address)
        address_entry.grid(column=1, row=2, padx=5, pady=5, sticky='w')

        # Pay button
        pay_button = ttk.Button(delivery_window, text="Pay", command=lambda: self.submit_order_delivery(customer_name.get(), phone_number.get(), delivery_address.get(), selected_items, delivery_window, parent_window))
        pay_button.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

    def submit_order_takeaway(self, customer_name, selected_items, window, parent_window):
        if not customer_name:
            tk.messagebox.showerror("Error", "Customer name is required for takeaway.")
            return

        order = self.restaurant.create_order(f"Takeaway for {customer_name}", "take-away", selected_items)
        tk.messagebox.showinfo("Order Created", f"Takeaway order created for {customer_name}, for ${order.total}")
        window.destroy()
        parent_window.destroy()

    def submit_order_delivery(self, customer_name, phone_number, delivery_address, selected_items, window, parent_window):
        phone_regex = r'^\+?\d{10,15}$'  # Adjust regex as needed
        address_regex = r'.{5,}'  # Adjust regex as needed

        if not customer_name:
            tk.messagebox.showerror("Error", "Customer name is required for delivery.")
            return
        if not tk.re.match(phone_regex, phone_number):
            tk.messagebox.showerror("Error", "Invalid phone number format.")
            return
        if not tk.re.match(address_regex, delivery_address):
            tk.messagebox.showerror("Error", "Invalid address format.")
            return

        order = self.restaurant.create_order(f"Delivery to {customer_name}", "delivery", selected_items)
        tk.messagebox.showinfo("Order Created", f"Delivery order created for {customer_name}, for ${order.total}")
        window.destroy()
        parent_window.destroy()

    def open_order_details_window(self, order):
        order_details_window = tk.Toplevel(self.master)
        order_details_window.title("Order Details")

        tk.Label(order_details_window, text=f"Table Number: {order.table_number}").pack()
        tk.Label(order_details_window, text=f"Order Type: {order.order_type}").pack()
        tk.Label(order_details_window, text="Items:").pack()
        for item in order.items:
            tk.Label(order_details_window, text=f"{item[0][1]} - ${item[0][2]}").pack()
        ttk.Button(order_details_window, text="Pay", command=lambda: self.pay_order(order)).pack()

    def pay_order(self, order):
        self.add_payment(order)

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
        reservation_time = ["12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00",
                            "20:30", "21:00", "21:30"]
        party_size = ["1","2","3","4","5","6","7","8","9+"]
        
        table_label = tk.Label(reservation_window, text="Table Number:")
        table_label.grid(row=0, column=0)
        table_number = tk.StringVar(reservation_window)
        table_entry = tk.OptionMenu(reservation_window, table_number, *table_numbers)
        #table_entry.current(0)
        table_entry.grid(row=0, column=1)

        time_label = tk.Label(reservation_window, text="Reservation Time:")
        time_label.grid(row=1, column=0)
        time_allocation = tk.StringVar(reservation_window)
        time_entry = tk.OptionMenu(reservation_window, time_allocation, *reservation_time)
        #table_entry.current(0)
        time_entry.grid(row=1, column=1)

        party_size_label = tk.Label(reservation_window, text="Party Size:")
        party_size_label.grid(row=2, column=0)
        party_size_selected = tk.StringVar(reservation_window)
        party_size_entry = tk.OptionMenu(reservation_window, party_size_selected, *party_size)
        #table_entry.current(0)
        party_size_entry.grid(row=2, column=1)
        
        party_name_label = tk.Label(reservation_window, text="Name")
        party_name_label.grid(row=3, column=0)
        party_name_entry = tk.Entry(reservation_window)
        party_name_entry.grid(row=3, column=1)
        
        submit_button = tk.Button(reservation_window, text="Submit",
                                  command=lambda: self.submit_reservation(reservation_window, table_number.get(),
                                                                          time_allocation.get(), party_size_selected.get(),party_name_entry.get()))
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

        menu_options = ["Food", "Dessert", "Drink"]

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
        item_type = tk.StringVar(add_item_window)
        type_select = tk.OptionMenu(add_item_window, item_type, *menu_options)
        type_select.grid(row=2, column=1)
        #type_entry = tk.Entry(add_item_window)
        #type_entry.grid(row=2, column=1)
    
        submit_button = tk.Button(add_item_window, text="Submit",
                                  command=lambda: self.submit_menu_item(add_item_window, name_entry.get(),
                                                                       price_entry.get(), item_type.get()))
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

    def add_payment(self, order):
        add_payment_window = tk.Toplevel(self.master)
        add_payment_window.title("Add Payment")

        card_button = tk.Button(add_payment_window, text="Card", 
                                command=lambda: self.submit_payment(add_payment_window, order, "card"))
        card_button.grid(row=3, columnspan=1)

        cash_button = tk.Button(add_payment_window, text="Cash", 
                                command=lambda: self.submit_payment(add_payment_window, order, "cash"))
        cash_button.grid(row=4, columnspan=1)

    def submit_payment(self, window, order, method):
        amount = order.total
        payment = self.restaurant.add_payment(order, amount, method)
        message = payment.make_payment()
        tk.messagebox.showinfo("Payment Window", message)
        window.destroy()