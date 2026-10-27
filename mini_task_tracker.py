"""Menu-based task tracker with JSON persistence."""
import json
from pathlib import Path

TASK_FILE = Path(__file__).resolve().parent / "tasks.json"
tasks = []


def load_tasks():
    """Load saved tasks or start with an empty list."""
    global tasks
    try:
        with TASK_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get("title"), str)
            or not isinstance(item.get("done"), bool)
            for item in data
        ):
            raise ValueError("Invalid task data format")
        tasks = data
        print(f"Loaded {len(tasks)} saved task(s).")
    except FileNotFoundError:
        tasks = []
        print("No saved tasks found. Starting fresh.")
    except (json.JSONDecodeError, ValueError, OSError) as error:
        tasks = []
        print(f"Could not load tasks ({error}). Starting with an empty list.")


def save_tasks():
    """Save the task list as JSON."""
    try:
        with TASK_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Error saving tasks: {error}")


def add_task():
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks()
    print("Task added.")


def view_tasks():
    if not tasks:
        print("No tasks available.")
        return
    for number, task in enumerate(tasks, start=1):
        status = "Done" if task["done"] else "Pending"
        print(f'{number}. {task["title"]} [{status}]')


def select_task_number():
    if not tasks:
        print("No tasks available.")
        return None
    try:
        number = int(input("Task number: "))
    except ValueError:
        print("Please enter a valid whole number.")
        return None
    if not 1 <= number <= len(tasks):
        print("Invalid task number.")
        return None
    return number - 1


def complete_task():
    index = select_task_number()
    if index is None:
        return
    tasks[index]["done"] = True
    save_tasks()
    print("Task completed.")


def delete_task():
    index = select_task_number()
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks()
    print(f'Task deleted: {removed["title"]}')


def main():
    load_tasks()
    while True:
        print("\n--- TASK TRACKER ---")
        print("1. Add   2. View   3. Complete   4. Delete   5. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
