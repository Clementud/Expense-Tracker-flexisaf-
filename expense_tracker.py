"""A small CSV-backed expense tracker suitable for running in PyCharm."""

from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "expenses.csv"
FIELDS = ("date", "category", "description", "amount")


class ExpenseFileError(Exception):
    """Raised when the expense data file cannot be read or written safely."""


def load_expenses(path: Path = DATA_FILE) -> list[dict[str, str]]:
    """Load and validate CSV rows. A missing file is a first-run empty ledger."""
    if not path.exists():
        return []
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None or not set(FIELDS).issubset(reader.fieldnames):
                raise ExpenseFileError(
                    "The CSV header is invalid. Expected columns: " + ", ".join(FIELDS)
                )
            rows = []
            for line_number, row in enumerate(reader, start=2):
                if not row or any(row.get(field) is None for field in FIELDS):
                    raise ExpenseFileError(f"Row {line_number} is incomplete.")
                try:
                    date.fromisoformat(row["date"].strip())
                    amount = Decimal(row["amount"].strip())
                    if not amount.is_finite() or amount <= 0:
                        raise InvalidOperation
                except (ValueError, InvalidOperation):
                    raise ExpenseFileError(
                        f"Row {line_number} has an invalid date or amount."
                    ) from None
                rows.append({field: row[field].strip() for field in FIELDS})
            return rows
    except (OSError, csv.Error, UnicodeError) as error:
        raise ExpenseFileError(f"Could not read '{path.name}': {error}") from error


def save_expenses(expenses: list[dict[str, str]], path: Path = DATA_FILE) -> None:
    """Write the complete ledger, reporting filesystem errors clearly."""
    try:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(expenses)
    except (OSError, csv.Error) as error:
        raise ExpenseFileError(f"Could not save '{path.name}': {error}") from error


def ask_expense() -> dict[str, str]:
    """Prompt until the user enters a valid expense."""
    while True:
        raw_date = input("Date (YYYY-MM-DD, blank for today): ").strip()
        if not raw_date:
            raw_date = date.today().isoformat()
        try:
            date.fromisoformat(raw_date)
        except ValueError:
            print("Please enter a real date in YYYY-MM-DD format.")
            continue
        category = input("Category: ").strip()
        description = input("Description: ").strip()
        if not category or not description:
            print("Category and description cannot be blank.")
            continue
        try:
            amount = Decimal(input("Amount: ").strip())
            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation
        except (ValueError, InvalidOperation):
            print("Enter an amount greater than zero, such as 12.50.")
            continue
        return {"date": raw_date, "category": category,
                "description": description, "amount": f"{amount:.2f}"}


def show_expenses(expenses: list[dict[str, str]]) -> None:
    if not expenses:
        print("No expenses yet.")
        return
    print("\nDate       | Category      | Description             | Amount")
    print("-" * 68)
    for item in expenses:
        print(f"{item['date']:<10} | {item['category']:<13} | "
              f"{item['description']:<23} | {Decimal(item['amount']):>8.2f}")
    total = sum((Decimal(item["amount"]) for item in expenses), Decimal("0"))
    print("-" * 68)
    print(f"Total: {total:.2f}\n")


def main() -> None:
    try:
        expenses = load_expenses()
    except ExpenseFileError as error:
        print(f"Data file problem: {error}")
        print("Fix the CSV header or row shown above, then run the program again.")
        return

    while True:
        print("\nExpense Tracker\n1. View expenses\n2. Add expense\n3. Exit")
        choice = input("Choose 1-3: ").strip()
        if choice == "1":
            show_expenses(expenses)
        elif choice == "2":
            expenses.append(ask_expense())
            try:
                save_expenses(expenses)
                print("Expense saved.")
            except ExpenseFileError as error:
                expenses.pop()
                print(f"Save problem: {error}")
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
