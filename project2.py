import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"
FIELDNAMES = ["Date", "Category", "Description", "Amount"]

CATEGORIES = [
    "Food", "Transport", "Shopping",
    "Health", "Entertainment", "Bills", "Other"
]


# ── File handling ────────────────────────────────────────────────────────────

def load_expenses():
    """Load expenses from CSV file into a list of dicts."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_expenses(expenses):
    """Save list of expense dicts to CSV file."""
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)
    print("  ✔  Saved to 'expenses.csv'")


# ── Helper ───────────────────────────────────────────────────────────────────

def get_amounts(expenses):
    return [float(e["Amount"]) for e in expenses]


def print_table(expenses):
    """Print expenses as a simple formatted table."""
    if not expenses:
        print("  No records found.")
        return
    print(f"\n  {'#':<4} {'Date':<12} {'Category':<15} {'Description':<20} {'Amount':>10}")
    print("  " + "-" * 65)
    for i, e in enumerate(expenses, 1):
        print(f"  {i:<4} {e['Date']:<12} {e['Category']:<15} {e['Description']:<20} {'Rs.'+e['Amount']:>10}")
    print("  " + "-" * 65)


# ── Features ─────────────────────────────────────────────────────────────────

def add_expense(expenses):
    print("\n--- Add Expense -------------------------------------------")

    date_input = input("  Date (YYYY-MM-DD) or press Enter for today: ").strip()
    expense_date = date.today().strftime("%Y-%m-%d") if not date_input else date_input

    print("  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        choice = input("  Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            category = CATEGORIES[int(choice) - 1]
            break
        print("  Invalid choice. Try again.")

    description = input("  Description: ").strip() or "-"

    while True:
        amt = input("  Amount (Rs.): ").strip()
        try:
            amount = float(amt)
            if amount > 0:
                break
        except ValueError:
            pass
        print("  Enter a valid positive number.")

    expenses.append({
        "Date": expense_date,
        "Category": category,
        "Description": description,
        "Amount": f"{amount:.2f}"
    })
    save_expenses(expenses)
    print(f"  Added: {category} - Rs.{amount:.2f}")


def view_all(expenses):
    print("\n--- All Expenses ------------------------------------------")
    print_table(expenses)
    if expenses:
        total = sum(get_amounts(expenses))
        print(f"  Total records : {len(expenses)}")
        print(f"  Grand Total   : Rs.{total:.2f}")


def summary_by_category(expenses):
    print("\n--- Summary by Category -----------------------------------")
    if not expenses:
        print("  No expenses to summarize.")
        return

    groups = {}
    for e in expenses:
        cat = e["Category"]
        amt = float(e["Amount"])
        groups.setdefault(cat, []).append(amt)

    print(f"\n  {'Category':<15} {'Entries':>8} {'Total (Rs.)':>12} {'Avg (Rs.)':>12}")
    print("  " + "-" * 50)
    for cat, amounts in sorted(groups.items()):
        total = sum(amounts)
        avg   = total / len(amounts)
        print(f"  {cat:<15} {len(amounts):>8} {total:>12.2f} {avg:>12.2f}")
    print("  " + "-" * 50)
    grand = sum(get_amounts(expenses))
    print(f"  {'Grand Total':<15} {len(expenses):>8} {grand:>12.2f}")


def monthly_summary(expenses):
    print("\n--- Monthly Summary ---------------------------------------")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    months = {}
    for e in expenses:
        month = e["Date"][:7]
        months.setdefault(month, 0)
        months[month] += float(e["Amount"])

    print(f"\n  {'Month':<12} {'Total (Rs.)':>12}")
    print("  " + "-" * 26)
    for month in sorted(months):
        print(f"  {month:<12} {months[month]:>12.2f}")


def filter_by_category(expenses):
    print("\n--- Filter by Category ------------------------------------")
    print("  Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    choice = input("  Choose category number: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
        cat = CATEGORIES[int(choice) - 1]
        filtered = [e for e in expenses if e["Category"] == cat]
        if not filtered:
            print(f"  No expenses found for '{cat}'.")
        else:
            print_table(filtered)
            total = sum(float(e["Amount"]) for e in filtered)
            print(f"  Total for {cat}: Rs.{total:.2f}")
    else:
        print("  Invalid choice.")


def delete_expense(expenses):
    print("\n--- Delete Expense ----------------------------------------")
    if not expenses:
        print("  No expenses to delete.")
        return

    print_table(expenses)
    idx = input("\n  Enter record number to delete (0 to cancel): ").strip()
    if idx.isdigit():
        idx = int(idx)
        if idx == 0:
            return
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            save_expenses(expenses)
            print(f"  Deleted: {removed['Category']} - Rs.{removed['Amount']}")
        else:
            print("  Record number out of range.")
    else:
        print("  Invalid input.")


def quick_stats(expenses):
    print("\n--- Quick Stats -------------------------------------------")
    if not expenses:
        print("  No data available.")
        return

    amounts = get_amounts(expenses)
    total   = sum(amounts)
    avg     = total / len(amounts)
    highest = max(amounts)
    lowest  = min(amounts)

    variance = sum((a - avg) ** 2 for a in amounts) / len(amounts)
    std_dev  = variance ** 0.5

    top = max(expenses, key=lambda e: float(e["Amount"]))

    print(f"  Total spent  : Rs.{total:.2f}")
    print(f"  Highest      : Rs.{highest:.2f}")
    print(f"  Lowest       : Rs.{lowest:.2f}")
    print(f"  Average      : Rs.{avg:.2f}")
    print(f"  Std deviation: Rs.{std_dev:.2f}")
    print(f"  Biggest spend: {top['Category']} - {top['Description']} (Rs.{top['Amount']})")


# ── Main menu ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("       Daily Expense Tracker")
    print("=" * 50)

    expenses = load_expenses()
    print(f"  Loaded {len(expenses)} existing record(s).")

    menu = {
        "1": ("Add Expense",          lambda: add_expense(expenses)),
        "2": ("View All Expenses",    lambda: view_all(expenses)),
        "3": ("Summary by Category",  lambda: summary_by_category(expenses)),
        "4": ("Monthly Summary",      lambda: monthly_summary(expenses)),
        "5": ("Filter by Category",   lambda: filter_by_category(expenses)),
        "6": ("Delete an Expense",    lambda: delete_expense(expenses)),
        "7": ("Quick Stats",          lambda: quick_stats(expenses)),
        "0": ("Exit",                 None),
    }

    while True:
        print("\n--- Menu ----------------------------------------------")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")

        choice = input("\n  Enter choice: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            break
        elif choice not in menu:
            print("  Invalid option. Try again.")
        else:
            _, action = menu[choice]
            action()


if __name__ == "__main__":
    main()
