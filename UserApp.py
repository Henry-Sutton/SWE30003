import tkinter as tk
import ttkbootstrap as ttk

class UserApp:
    def __init__(self, master):
        self.master = master
        #self.username = username
        #self.password = password
        self.master.geometry("400x400")
        master.title("Restaurant Management System")

        self.anchor = ttk.Label(master, text="")
        self.anchor.pack(pady=40)

        self.label = ttk.Label(master, text="Enter your user ID")
        self.label.pack(padx=50, pady=5)

        user_entry = tk.Entry(master)
        user_entry.pack(padx=50, pady=5)
        
        self.login_button = ttk.Button(master, text="login", command=self.login)
        self.login_button.pack(padx=50, pady=5)

    def login(self):
        self.master = self
        