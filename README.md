# Expense Tracker

A simple desktop GUI application built with **Python**, **Tkinter**, and **SQLite** to help you log and manage your daily expenses.

---

## Features

-  Add expenses with amount, category, description, and date
-  View all saved expenses in a sortable table
-  Delete selected expenses with confirmation
-  Data is saved locally in an SQLite database (`expenses.db`)
-  Simple and intuitive interface built with Tkinter

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

## Screenshots

*(You can add screenshots here if you want)*

---

## Technologies Used

- [Python 3.x](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – for GUI
- [SQLite3](https://www.sqlite.org/index.html) – for data persistence
- [os](https://docs.python.org/3/library/os.html) and [datetime](https://docs.python.org/3/library/datetime.html)

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

---

## Future Ideas

- [ ] Edit/update existing expenses
- [ ] Show total expenses per day/month
- [ ] Filter by category or date
- [ ] Export to CSV or Excel
- [ ] Visualize data using graphs (e.g. pie chart)
