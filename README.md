# Expense Tracker

A simple Python expense tracker that runs in PyCharm and stores entries in a CSV file. It uses only Python's standard library.

## Run in PyCharm

1. Open the `expense_tracker` folder in PyCharm.
2. Open `expense_tracker.py` and choose **Run 'expense_tracker'**.
3. Choose **1** to view the sample entries, **2** to add an expense, or **3** to exit.

Python 3.10 or newer is recommended. The CSV path is based on the script's folder, so the app does not depend on PyCharm's working-directory setting.

## Sample data

`expenses.csv` is the starter file. Keep its header exactly as:

```csv
date,category,description,amount
```

Dates use `YYYY-MM-DD`; amounts must be positive numbers. If the file is absent, the tracker starts with an empty ledger and creates the file when the first expense is saved.

## Demo and error-handling evidence

Open `demo.py` in PyCharm and run it to see the sample ledger and a controlled invalid-header example. Expected error output:

```text
=== Error handling: invalid CSV header ===
Handled safely: The CSV header is invalid. Expected columns: date, category, description, amount
The original sample file was not changed.
```

The app also reports incomplete rows, invalid dates or amounts, unreadable files, and save failures without showing a traceback to the user. For an invalid real `expenses.csv`, correct the row or restore the header shown above and rerun the program.
