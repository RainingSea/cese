class TaskManager:
    def __init__(self):
        self.tasks = []
        self.members = []
        self.notifications = []

    def create_task(self, title: str, description: str, deadline: str, priority: str) -> None:
        task = {
            "title": title,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "status": "pending"
        }
        self.tasks.append(task)
        self.save_data()

    def assign_task(self, task_id: int, member_id: int) -> None:
        if task_id < len(self.tasks) and member_id < len(self.members):
            self.tasks[task_id]['assigned_to'] = self.members[member_id]
            self.save_data()

    def update_progress(self, task_id: int, status: str) -> None:
        if task_id < len(self.tasks):
            self.tasks[task_id]['status'] = status
            self.save_data()

    def send_notification(self, message: str) -> None:
        self.notifications.append(message)
        self.save_data()

    def load_data(self) -> None:
        with open('tasks.txt', 'r') as task_file:
            for line in task_file:
                title, description, deadline, priority, status = line.strip().split('|')
                self.tasks.append({
                    "title": title,
                    "description": description,
                    "deadline": deadline,
                    "priority": priority,
                    "status": status
                })

        with open('members.txt', 'r') as member_file:
            self.members = [line.strip() for line in member_file]

        with open('notifications.txt', 'r') as notification_file:
            self.notifications = [line.strip() for line in notification_file]

    def save_data(self) -> None:
        with open('tasks.txt', 'w') as task_file:
            for task in self.tasks:
                task_file.write(f"{task['title']}|{task['description']}|{task['deadline']}|{task['priority']}|{task['status']}\n")

        with open('members.txt', 'w') as member_file:
            for member in self.members:
                member_file.write(f"{member}\n")

        with open('notifications.txt', 'w') as notification_file:
            for notification in self.notifications:
                notification_file.write(f"{notification}\n")