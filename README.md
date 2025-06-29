# Expense Tracker

A simple desktop GUI application built with **Python**, **Tkinter**, and **SQLite** to help you log and manage your daily expenses.

---

## Features

- Add expenses with amount, category, description, and date
- Choose categories like Food, Transport, Entertainment, etc.
- Auto-fill today’s date, or manually enter a different one
- Data is saved locally in an SQLite database (`expenses.db`)
- Simple and intuitive interface built with Tkinter

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

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ilbeykirbas/expenses-app/blob/main/LICENSE) file for details.

---

## Author

Developed by İlbey Kırbaş
GitHub: @ilbeykirbas https://github.com/ilbeykirbas

---

## Future Ideas

- [ ] View all expenses in a table
- [ ] Filter expenses by date or category
- [ ] Monthly total or average calculations
- [ ] Graph support using `matplotlib`
