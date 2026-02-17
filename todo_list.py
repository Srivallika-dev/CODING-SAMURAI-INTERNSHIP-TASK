"""
To-Do List Manager
Author: Your Name
Description:
A simple command-line To-Do List application that allows users
to add, view, complete, and delete tasks.
"""

def add_task(tasks):
    task = input("Enter new task: ").strip()
    if task:
        tasks.append({"task": task, "completed": False})
        print("Task added successfully.")
    else:
        print("Task cannot be empty.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\n===== Your To-Do List =====")
    for index, task in enumerate(tasks, start=1):
        status = "✔" if task["completed"] else "✘"
        print(f"{index}. [{status}] {task['task']}")


def complete_task(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter task number to mark as completed: "))
        if 1 <= task_number <= len(tasks):
            tasks[task_number - 1]["completed"] = True
            print("Task marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_number = int(input("Enter task number to delete: "))
        if 1 <= task_number <= len(tasks):
            removed_task = tasks.pop(task_number - 1)
            print(f"Deleted task: {removed_task['task']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    tasks = []

    while True:
        print("\n===== To-Do List Menu =====")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Exiting To-Do List. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
