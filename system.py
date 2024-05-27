import sqlite3
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

from MenuItem import MenuItem
from Order import Order
from Reservation import Reservation
from User import User
from Restaurant import Restaurant
from RestaurantApp import RestaurantApp

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


if __name__ == "__main__":
    restaurant = Restaurant(c, conn)
    root = ttk.window.Window(size=[800, 420])
    app = RestaurantApp(root, restaurant)
    root.mainloop()

# Close the database connection
conn.close()
