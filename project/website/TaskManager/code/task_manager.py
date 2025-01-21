class TaskManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.tasks = {}

    def load_tasks(self, username: str):
        """Load tasks from the tasks.txt file for a specific user."""
        tasks_data = self.file_handler.read_file('tasks.txt')
        for line in tasks_data:
            user, description, due_date = line.strip().split('|')
            if user not in self.tasks:
                self.tasks[user] = []
            self.tasks[user].append({'description': description, 'due_date': due_date})

    def add_task(self, username: str, description: str, due_date: str):
        """Add a new task for a specific user."""
        if username not in self.tasks:
            self.tasks[username] = []
        self.tasks[username].append({'description': description, 'due_date': due_date})
        self.file_handler.append_to_file('tasks.txt', f"{username}|{description}|{due_date}")

    def remove_task(self, username: str, task_id: int):
        """Remove a task by its ID for a specific user."""
        if username in self.tasks and 0 <= task_id < len(self.tasks[username]):
            del self.tasks[username][task_id]
            self.save_tasks()

    def get_tasks(self, username: str) -> list:
        """Get all tasks for a specific user."""
        return self.tasks.get(username, [])

    def save_tasks(self):
        """Save all tasks to the tasks.txt file."""
        all_tasks = []
        for user, tasks in self.tasks.items():
            for task in tasks:
                all_tasks.append(f"{user}|{task['description']}|{task['due_date']}")
        self.file_handler.write_file('tasks.txt', all_tasks)