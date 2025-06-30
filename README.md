# Expense Tracker

A simple desktop GUI application built with **Python**, **Tkinter**, and **SQLite** to help you log and manage your daily expenses.

---

## Features

- Save your expenses with amount, category, description and date
- View expenses in a sortable table (Treeview)
- Automatically calculates and displays total spending
- Filter expenses by category and date range
- Select and update existing expense records
- Delete selected expenses with confirmation
- View category-wise spending distribution in a pie chart
- Stores all data locally using SQLite (`data/expenses.db`)
- Clean and responsive user interface with Tkinter

---

## Project Structure

```
expense-tracker/
├── src/
│   └── expense_app.py        # Main GUI application
├── data/
│   └── expenses.db           # SQLite database (auto-created)
├── .gitignore                # To exclude data/expenses.db
├── README.md                 # This file
├── LICENSE                   # MIT license (or your choice)
```

> `data/` folder is created automatically if missing.

---

## Technologies Used

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – for GUI
- [SQLite3](https://www.sqlite.org/index.html) – for data persistence
- [os](https://docs.python.org/3/library/os.html) and [datetime](https://docs.python.org/3/library/datetime.html)
- [matplotlib](https://pypi.org/project/matplotlib/) for chart display

---

## How to Run

1. Clone or download the repository.
2. Make sure Python is installed on your system.
3. Navigate to the `src` folder and run the app:

```bash
cd src
python expense_app.py
```

> All data will be saved in `../data/expenses.db`

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ilbeykirbas/expense-app/blob/main/LICENSE) file for details.

---

## Author

Developed by İlbey Kırbaş  
GitHub: [@ilbeykirbas](https://github.com/ilbeykirbas)
