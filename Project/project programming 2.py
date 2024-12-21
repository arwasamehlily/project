from abc import ABC, abstractmethod
from datetime import datetime

class Task:
    """Class for adding and updating task status"""
    def __init__(self, title, priority="Medium"):
        self.title = title
        self.completed = False
        self.priority = priority
        self.created_at = datetime.now()

    def update_status(self, status):
        """Update task status"""
        self.completed = status

class Reminder:
    """Class for sending reminders"""
    def __init__(self, reminder_type):
        self.reminder_type = reminder_type  # Type of reminder (SMS or Email)

    def send_reminder(self, task):
        """Send a reminder for the task"""
        print(f"Reminder sent for task: {task.title} via {self.reminder_type}")


# OCP: Adding new features like priority without modifying the core code
class PriorityTask(Task):
    """Class for setting task priorities"""
    def __init__(self, title, priority="High"):
        super().__init__(title, priority)


# LSP: Handling all types of tasks in the same way
class RecurringTask(Task):
    """Class for recurring tasks"""
    def __init__(self, title, recurrence):
        super().__init__(title)
        self.recurrence = recurrence  # Recurrence (daily, weekly, monthly)

# ISP: Splitting interfaces to separately manage tasks and reminders
class TaskManager:
    """Interface for managing tasks"""
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        """Add a task"""
        self.tasks.append(task)

    def show_tasks(self):
        """Display all tasks"""
        for idx, task in enumerate(self.tasks, 1):
            status = "Completed" if task.completed else "Pending"
            print(f"{idx}. {task.title} (Priority: {task.priority}, Status: {status})")


class ReminderManager:
    """Interface for managing reminders"""
    def __init__(self, reminder):
        self.reminder = reminder

    def send_task_reminders(self, tasks):
        """Send reminders for incomplete tasks"""
        for task in tasks:
            if not task.completed:
                self.reminder.send_reminder(task)


# DIP: Separating reminder logic from the main application
class EmailReminder(Reminder):
    """Reminder via Email"""
    def __init__(self):
        super().__init__("Email")


class SMSReminder(Reminder):
    """Reminder via SMS"""
    def __init__(self):
        super().__init__("SMS")


# Application execution example
if __name__ == "__main__":
    # Create tasks
    task1 = Task("Study Data Structures", "High")
    task2 = RecurringTask("Exercise", "Daily")
    task3 = PriorityTask("Complete Python Project")

    # Task management
    task_manager = TaskManager()
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    task_manager.add_task(task3)

    print("\n--- To-Do List ---")
    task_manager.show_tasks()

    # Send reminders
    email_reminder = EmailReminder()
    reminder_manager = ReminderManager(email_reminder)
    reminder_manager.send_task_reminders(task_manager.tasks)

    # Update task status and show the list again
    task1.update_status(True)
    print("\n--- Updated To-Do List ---")
    task_manager.show_tasks()
