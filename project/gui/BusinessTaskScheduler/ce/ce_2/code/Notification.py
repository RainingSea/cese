from datetime import datetime, timedelta

class Notification:
    def send_notification(self, task) -> None:
        deadline = datetime.strptime(task.deadline, '%Y-%m-%d')
        if deadline <= datetime.now() + timedelta(days=1):
            print(f"Reminder: Task '{task.title}' is due on {task.deadline}.")