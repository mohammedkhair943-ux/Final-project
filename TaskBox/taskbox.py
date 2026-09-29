from datetime import datetime


class Task:
    def __init__(self, title, priority="Medium"):
        self.title = title
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def complete(self):
        self.completed = True

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.title} | Priority: {self.priority}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority="Medium"):
        self.tasks.append(Task(title, priority))

    def complete_task(self, number):
        if 1 <= number <= len(self.tasks):
            self.tasks[number - 1].complete()
            return True
        return False

    def show_tasks(self):
        if not self.tasks:
            print("\nNo tasks yet.")
            return
        print("\n Tasks")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def show_progress(self):
        total = len(self.tasks)
        done = sum(task.completed for task in self.tasks)
        print(f"\nProgress: {done}/{total} completed")


def main():
    manager = TaskManager()

    while True:
        print("\n TaskBox ")
        print("1. Add task")
        print("2. Show tasks")
        print("3. Complete task")
        print("4. Show progress")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                continue

            priority = input("Priority (Low/Medium/High): ").strip().capitalize()
            if priority not in {"Low", "Medium", "High"}:
                priority = "Medium"

            manager.add_task(title, priority)
            print("Task added.")

        elif choice == "2":
            manager.show_tasks()

        elif choice == "3":
            manager.show_tasks()
            if manager.tasks:
                try:
                    number = int(input("Task number to complete: "))
                    if manager.complete_task(number):
                        print("Task completed.")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a number.")

        elif choice == "4":
            manager.show_progress()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
