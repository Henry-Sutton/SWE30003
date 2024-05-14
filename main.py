
import tkinter as tk
from tkinter import messagebox

# import classes
from Restaurant import Restaurant
from Database import Database
from RestaurantGUI import RestaurantGUI

def main():
    restaurant = Restaurant()
    database = Database('restaurant.db')
    gui = RestaurantGUI(tk.tk())
    gui.run

if __name__ == "__main__":
    main()

