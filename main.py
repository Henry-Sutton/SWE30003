
import tkinter as tk
from tkinter import messagebox

# import classes
from Restaurant import Restaurant
from Database import Database
from RestaurantGUI import RestaurantGUI

def main():
    root = tk.Tk()
    database = Database('restaurant.db')
    gui = RestaurantGUI(root)
    gui.run()

if __name__ == "__main__":
    main()

