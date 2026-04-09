import csv
import os
from datetime import date

FILE_NAME = "tasks.csv"
FIELDNAMES = ["ID", "Title", "Description", "Priority", "Status", "Due Date"]

PRIORITIES = ["High", "Medium", "Low"]
STATUSES   = ["Pending", "In Progress", "Done"]


# ── File Handling ─────────────────────────────────────────────────────────────

def load_tasks():
    """Load tasks from CSV into a list of dicts."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_tasks(tasks):
    """Save list of task dicts to CSV."""
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tasks)


def next_id(tasks):
    """Generate the next unique task ID."""
    if not tasks:
        return 1
    return max(int(t["ID"]) for t in tasks) + 1


# ── Display ───────────────────────────────────────────────────────────────────

def print_table(tasks):
    """Print tasks as a formatted table."""
    if not tasks:
        print("  No tasks found.")
        return
    print(f"\n  {'ID':<5} {'Title':<22} {'Priority':<10} {'Status':<12} {'Due Date':<12} {'Description'}")
    print("  " + "-" * 85)
    for t in tasks:
        print(
            f"  {t['ID']:<5} {t['Title']:<22} {t['Priority']:<10} "
            f"{t['Status']:<12} {t['Due Date']:<12} {t['Description']}"
        )
    print("  " + "-" * 85)


# ── Core Features ─────────────────────────────────────────────────────────────

def add_task(tasks):
    print("\n--- Add Task ----------------------------------------------")

    title = input("  Title: ").strip()
    if not title:
        print("  Title cannot be empty.")
        return

    description = input("  Description (optional): ").strip() or "-"

    print("  Priority:")
    for i, p in enumerate(PRIORITIES, 1):
        print(f"    {i}. {p}")
    while True:
        choice = input("  Choose priority (1-3): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 3:
            priority = PRIORITIES[int(choice) - 1]
            break
        print("  Invalid choice.")

    due = input("  Due Date (YYYY-MM-DD) or Enter to skip: ").strip()
    due_date = due if due else "-"

    tasks.append({
        "ID":          next_id(tasks),
        "Title":       title,
        "Description": description,
        "Priority":    priority,
        "Status":      "Pending",
        "Due Date":    due_date,
    })
    save_tasks(tasks)
    print(f"  Task '{title}' added successfully.")


def view_tasks(tasks):
    print("\n--- All Tasks ---------------------------------------------")
    print_table(tasks)
    if tasks:
        total   = len(tasks)
        pending = sum(1 for t in tasks if t["Status"] == "Pending")
        in_prog = sum(1 for t in tasks if t["Status"] == "In Progress")
        done    = sum(1 for t in tasks if t["Status"] == "Done")
        print(f"\n  Total: {total}  |  Pending: {pending}  |  In Progress: {in_prog}  |  Done: {done}")


def delete_task(tasks):
    print("\n--- Delete Task -------------------------------------------")
    if not tasks:
        print("  No tasks to delete.")
        return

    print_table(tasks)
    tid = input("\n  Enter Task ID to delete (0 to cancel): ").strip()
    if tid == "0":
        return
    matches = [t for t in tasks if t["ID"] == tid]
    if not matches:
        print("  Task ID not found.")
        return
    tasks.remove(matches[0])
    save_tasks(tasks)
    print(f"  Task ID {tid} deleted.")


def update_status(tasks):
    print("\n--- Update Task Status ------------------------------------")
    if not tasks:
        print("  No tasks available.")
        return

    print_table(tasks)
    tid = input("\n  Enter Task ID to update (0 to cancel): ").strip()
    if tid == "0":
        return
    matches = [t for t in tasks if t["ID"] == tid]
    if not matches:
        print("  Task ID not found.")
        return

    task = matches[0]
    print(f"  Current status: {task['Status']}")
    print("  New Status:")
    for i, s in enumerate(STATUSES, 1):
        print(f"    {i}. {s}")
    while True:
        choice = input("  Choose status (1-3): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 3:
            task["Status"] = STATUSES[int(choice) - 1]
            break
        print("  Invalid choice.")

    save_tasks(tasks)
    print(f"  Task '{task['Title']}' status updated to '{task['Status']}'.")


def filter_tasks(tasks):
    print("\n--- Filter Tasks ------------------------------------------")
    print("  Filter by:")
    print("    1. Priority")
    print("    2. Status")
    choice = input("  Choose (1/2): ").strip()

    if choice == "1":
        print("  Priority:")
        for i, p in enumerate(PRIORITIES, 1):
            print(f"    {i}. {p}")
        c = input("  Choose (1-3): ").strip()
        if c.isdigit() and 1 <= int(c) <= 3:
            filtered = [t for t in tasks if t["Priority"] == PRIORITIES[int(c) - 1]]
            print_table(filtered)
        else:
            print("  Invalid choice.")

    elif choice == "2":
        print("  Status:")
        for i, s in enumerate(STATUSES, 1):
            print(f"    {i}. {s}")
        c = input("  Choose (1-3): ").strip()
        if c.isdigit() and 1 <= int(c) <= 3:
            filtered = [t for t in tasks if t["Status"] == STATUSES[int(c) - 1]]
            print_table(filtered)
        else:
            print("  Invalid choice.")
    else:
        print("  Invalid choice.")


def search_task(tasks):
    print("\n--- Search Task -------------------------------------------")
    keyword = input("  Enter keyword to search: ").strip().lower()
    if not keyword:
        print("  No keyword entered.")
        return
    results = [
        t for t in tasks
        if keyword in t["Title"].lower() or keyword in t["Description"].lower()
    ]
    if results:
        print_table(results)
        print(f"  {len(results)} result(s) found.")
    else:
        print("  No matching tasks found.")


def clear_done(tasks):
    print("\n--- Clear Completed Tasks ---------------------------------")
    done = [t for t in tasks if t["Status"] == "Done"]
    if not done:
        print("  No completed tasks to clear.")
        return
    confirm = input(f"  Remove {len(done)} completed task(s)? (y/n): ").strip().lower()
    if confirm == "y":
        tasks[:] = [t for t in tasks if t["Status"] != "Done"]
        save_tasks(tasks)
        print(f"  {len(done)} completed task(s) removed.")
    else:
        print("  Cancelled.")


# ── Main Menu ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("         Task Manager CLI")
    print("=" * 50)

    tasks = load_tasks()
    print(f"  Loaded {len(tasks)} existing task(s).")

    menu = {
        "1": ("Add Task",              lambda: add_task(tasks)),
        "2": ("View All Tasks",        lambda: view_tasks(tasks)),
        "3": ("Delete Task",           lambda: delete_task(tasks)),
        "4": ("Update Task Status",    lambda: update_status(tasks)),
        "5": ("Filter Tasks",          lambda: filter_tasks(tasks)),
        "6": ("Search Task",           lambda: search_task(tasks)),
        "7": ("Clear Completed Tasks", lambda: clear_done(tasks)),
        "0": ("Exit",                  None),
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