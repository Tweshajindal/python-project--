# Simple To-Do List Application

tasks = []

while True:
    print("\n----- TO DO LIST -----")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        if len(tasks) == 0:
            print("No tasks in the list.")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")

    elif choice == "2":
        task = input("Enter the task: ")
        tasks.append(task)
        print("Task added successfully!")

    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks to remove.")
        else:
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task}")
            try:
                task_no = int(input("Enter task number to remove: "))
                removed = tasks.pop(task_no - 1)
                print(f"Task '{removed}' removed.")
            except:
                print("Invalid task number.")

    elif choice == "4":
        print("Exiting To-Do List App.")
        break

    else:
        print("Invalid choice. Try again.")