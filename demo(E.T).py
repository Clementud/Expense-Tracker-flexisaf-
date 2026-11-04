"""Demonstrate normal sample-data loading and clear malformed-file handling."""

import tempfile
from pathlib import Path

from expense_tracker import ExpenseFileError, load_expenses, show_expenses


def main() -> None:
    sample = Path(__file__).resolve().parent / "expenses.csv"
    print("=== Normal sample data ===")
    expenses = load_expenses(sample)
    show_expenses(expenses)

    print("=== Error handling: invalid CSV header ===")
    with tempfile.TemporaryDirectory() as folder:
        broken_file = Path(folder) / "broken.csv"
        broken_file.write_text("wrong,columns\nvalue,value\n", encoding="utf-8")
        try:
            load_expenses(broken_file)
        except ExpenseFileError as error:
            print(f"Handled safely: {error}")
            print("The original sample file was not changed.")


if __name__ == "__main__":
    main()
