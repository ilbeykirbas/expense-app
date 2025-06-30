import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os
from datetime import date

class ExpenseApp:
    def __init__(self):
        self.setup_database()

        self.selected_id = None # No expense was chosen at first

        self.window = tk.Tk()
        self.window.title("Expense Tracker")
        self.window.geometry("450x600")

        # Amount
        tk.Label(self.window, text="Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        #Category
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

        # Add expense button
        tk.Button(self.window, text="Add Expense", command=self.add_expense).grid(row=4, column=1, sticky="e", padx=5, pady=5)

        # Delete expense button
        tk.Button(self.window, text="Delete Selected Expense", command=self.delete_expense).grid(row=5, column=0, padx=5, pady=5)
        
        # Update expense button
        tk.Button(self.window, text="Update Selected Expense", command=self.update_expense).grid(row=5, column=2, padx=5, pady=5)

        # Expenses list title
        tk.Label(self.window, text="Expenses:").grid(row=6, column=0, padx=5, pady=(10, 0), sticky="w")
        
        # Treeview table
        self.tree = ttk.Treeview(self.window, columns=("Amount", "Category", "Description", "Date"), show="headings", height=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        self.total_label = tk.Label(self.window, text="Total: $0.00", font=("Arial", 10, "bold"))
        self.total_label.grid(row=8, column=0, columnspan=3, pady=(5, 10), sticky="w")

        # Filter Controls
        tk.Label(self.window, text="Filter by Category:").grid(row=9, column=0, sticky="e", padx=5)
        self.filter_category = tk.StringVar()
        self.filter_category.set("All")
        tk.OptionMenu(self.window, self.filter_category, "General", "Food", "Transport", "Entertainment", "Utilities", "Other").grid(row=9, column=1, sticky="w", padx=5)

        tk.Label(self.window, text="Date Start:").grid(row=10, column=0, sticky="e", padx=5)
        self.filter_date_start = tk.Entry(self.window)
        self.filter_date_start.grid(row=10, column=1, padx=5)

        tk.Label(self.window, text="Date End:").grid(row=11, column=0, sticky="e", padx=5)
        self.filter_date_end = tk.Entry(self.window)
        self.filter_date_end.grid(row=11, column=1, padx=5)

        tk.Button(self.window, text="Filter", command=self.apply_filter).grid(row=12, column=1, sticky="e", padx=5, pady=5)
        tk.Button(self.window, text="Clear Filter", command=self.clear_filter).grid(row=12, column=0, sticky="w", padx=5, pady=5)
        tk.Button(self.window, text="Show Chart", command=self.show_chart).grid(row=13, column=1, pady=10)

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
        
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total = self.cursor.fetchone()[0] or 0
        self.total_label.config(text=f"Total: ${total:.2f}")

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

    def on_row_select(self, event):
        selected = self.tree.selection()
        if selected:
            expense_id = selected[0]
            self.cursor.execute("SELECT amount, category, description, date FROM expenses WHERE id=?", (expense_id,))
            row = self.cursor.fetchone()
            if row:
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, row[0])

                self.category_var.set(row[1])

                self.description_entry.delete(0, tk.END)
                self.description_entry.insert(0, row[2])

                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, row[3])

                self.selected_id = expense_id # Save it for update

    def update_expense(self):
        if self.selected_id is not None:
            try:
                amount = float(self.amount_entry.get())
                category = self.category_var.get()
                description = self.description_entry.get().strip()
                date_str = self.date_entry.get().strip()

                if not date_str:
                    raise ValueError("Date cannot be empty.")
                
                self.cursor.execute("""
                    UPDATE expenses
                    SET amount=?, category=?, description=?, date=?
                    WHERE id=?
                """, (amount, category, description, date_str, self.selected_id))
                self.conn.commit()

                self.status_label.config(text="Expense updated.", fg="green")
                self.load_expenses() 
                del self.selected_id # Forget after update is completed
            except ValueError:
                self.status_label.config(text="Please enter valid data.", fg="yellow")
        else:
            self.status_label.config(text="No row selected to update.", fg="yellow")

    def apply_filter(self):
        category = self.filter_category.get()
        start_date = self.filter_date_start.get().strip()
        end_date = self.filter_date_end.get().strip()

        query = "SELECT id, amount, category, description, date FROM expenses WHERE 1=1"
        params = []

        if category != "All":
            query += " AND category=?"
            params.append(category)
        
        if start_date:
            query += " AND date>=?"
            params.append(start_date)
        
        if end_date:
            query += " AND date<=?"
            params.append(end_date)

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row[1:], iid=row[0])

        self.cursor.execute(f"SELECT SUM(amount) FROM expenses WHERE id IN ({','.join(str(r[0]) for r in rows)})")
        total = self.cursor.fetchone()[0] or 0
        self.total_label.config(text=f"Total: ${total:.2f}")

    def clear_filter(self):
        self.filter_category.set("All")
        self.filter_date_start.delete(0, tk.END)
        self.filter_date_end.delete(0, tk.END)
        self.load_expenses()

    def show_chart(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("No data", "No expenses to display")
            return
        
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title("Expense Distribution by Category")
        plt.axis("equal")
        plt.show()

if __name__ == "__main__":
    ExpenseApp()
