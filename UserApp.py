import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from Restaurant import Restaurant
from RestaurantApp import RestaurantApp

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()

class UserApp:
    def __init__(self, master):
        self.master = master
        self.correct_user_id = "admin"
        self.master.geometry("400x400")
        master.title("Restaurant Management System")

        self.anchor = ttk.Label(master, text="")
        self.anchor.pack(pady=40)

        self.label = ttk.Label(master, text="Enter your user ID")
        self.label.pack(padx=50, pady=5)

        self.label = ttk.Label(master, text="ONLY WORKS WITH 'admin' CURRENTLY")
        self.label.pack(padx=50, pady=5)

        self.user_entry = tk.Entry(master)
        self.user_entry.pack(padx=50, pady=5)
        
        self.login_button = ttk.Button(master, text="login", command=self.login)
        self.login_button.pack(padx=50, pady=5)

        self.message_label = ttk.Label(master, text="")  # Create a single message label
        self.message_label.pack(pady=5)

    def login(self):
        entered_user_id = self.user_entry.get()
        if entered_user_id == self.correct_user_id:
            # self.message_label.config(text="login successful!", foreground="green")
            self.master.after(400, self.master.destroy)
            restaurant = Restaurant(c, conn)
            root = ttk.window.Window(size=[640, 480])
            app = RestaurantApp(root, restaurant)
            root.mainloop()
        else:
            self.message_label.config(text="Invalid User ID.", foreground="red")