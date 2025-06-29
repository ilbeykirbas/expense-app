import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from datetime import date

class ExpenseApp:
    def __init__(self):
        self.setup_database()

        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("400x250")

        tk.Label(self.window, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar(self.window)
        self.category_var.set("General")
        self.category_menu = tk.OptionMenu(self.window, self.category_var, "Food", "Transport", "Entertainment", "Utilities", "Other")
        self.category_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Description:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.description_entry = tk.Entry(self.window)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(self.window)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.window, text="Add Expense", command=self.add_expense).grid(row=4, column=1, sticky="e", padx=5, pady=5)

        self.status_label = tk.Label(self.window, text="")
        self.status_label.grid(row=5, column=1)

        self.window.mainloop()
    
    def setup_database(self):
        data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_folder, exist_ok=True)
        db_path = os.path.join(data_folder, "expenses.db")

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,    
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )     
        """)
        self.conn.commit()
    
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get().strip()
            date = self.date_entry.get().strip()

            if not date:
                raise ValueError("Date cannot be empty.")

            self.cursor.execute("""
                INSERT INTO expenses (amount, category, description, date)
                VALUES(?, ?, ?, ?)
            """, (amount, category, description, date)) 
            self.conn.commit()

            self.status_label.config(text="Expense added successfully.", fg="green")
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

        except ValueError:
            self.status_label.config(text="Please enter a valid amount and date.", fg="yellow")

if __name__ == "__main__":
    ExpenseApp()
