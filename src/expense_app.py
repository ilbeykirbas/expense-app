import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os
from datetime import date

class ExpenseApp:
    def __init__(self):
        self.setup_database()

        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("375x375")

        # Amount
        tk.Label(self.window, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Category
        tk.Label(self.window, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.category_var = tk.StringVar(self.window)
        self.category_var.set("General")
        self.category_menu = tk.OptionMenu(self.window, self.category_var, "Food", "Transport", "Entertainment", "Utilities", "Other")
        self.category_menu.grid(row=1, column=1, padx=5, pady=5)

        # Description
        tk.Label(self.window, text="Description:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.description_entry = tk.Entry(self.window)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Date
        tk.Label(self.window, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(self.window)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Add Button
        tk.Button(self.window, text="Add Expense", command=self.add_expense).grid(row=4, column=1, sticky="e", padx=5, pady=5)

        # Delete Button
        tk.Button(self.window, text="Delete Selected Expense", command=self.delete_expense).grid(row=5, column=0, padx=5, pady=5)
        
        # Expenses list title
        tk.Label(self.window, text="Expenses:").grid(row=6, column=0, padx=5, pady=(10, 0), sticky="w")
        
        # Treeview table
        self.tree = ttk.Treeview(self.window, columns=("Amount", "Category", "Description", "Date"), show="headings", height=5)
        self.tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        for col in ("Amount", "Category", "Description", "Date"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=90)

        self.load_expenses()

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
        
        self.load_expenses() # Update the table

    def load_expenses(self):
        # Delete current data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch the expenses from the database
        self.cursor.execute("SELECT id, amount, category, description, date FROM expenses ORDER BY id DESC")
        rows = self.cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row[1:], iid=row[0])

    def delete_expense(self):
        selected = self.tree.selection()
        if selected:
            expense_id = selected[0]
            confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected expense?")
            if confirm:
                self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
                self.conn.commit()
                self.load_expenses()
                self.status_label.config(text="Expense deleted.", fg="green")
        else:
            self.status_label.config(text="Please select a row to delete.", fg="yellow")

if __name__ == "__main__":
    ExpenseApp()
