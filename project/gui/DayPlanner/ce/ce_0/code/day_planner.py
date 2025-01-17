from task import Task
from category import Category
from reminder import Reminder

class DayPlanner:
    def __init__(self):
        self.tasks = Task.load()
        self.categories = Category.load()
        self.reminders = Reminder.get_reminders()

    def add_task(self, title: str, priority: int, category: str, time_slot: str):
        task = Task(title, priority, category, time_slot)
        task.save()
        self.tasks.append([title, priority, category, time_slot])

    def view_tasks(self) -> list:
        return self.tasks

    def set_priority(self, task_id: int, priority: int):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id][1] = priority
            self._save_tasks()

    def categorize_task(self, task_id: int, category: str):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id][2] = category
            self._save_tasks()

    def allocate_time(self, task_id: int, time_slot: str):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id][3] = time_slot
            self._save_tasks()

    def show_overview(self):
        return self.view_tasks()

    def _save_tasks(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write('|'.join(map(str, task)) + '\n')