from task import Task

class TaskManager:
    def __init__(self, username):
        self.username = username

    def load_tasks(self):
        tasks = []
        try:
            with open(f'tasks_{self.username}.txt', 'r') as f:
                for line in f:
                    task_info = line.strip().split('|')
                    tasks.append({'id': len(tasks), 'description': task_info[0], 'due_date': task_info[1]})
        except FileNotFoundError:
            pass
        return tasks

    def save_tasks(self, tasks):
        with open(f'tasks_{self.username}.txt', 'w') as f:
            for task in tasks:
                f.write(f"{task.description}|{task.due_date}\n")
        return True

    def add_task(self, description, due_date):
        task = Task(description, due_date)
        tasks = self.load_tasks()
        tasks.append(task)
        return self.save_tasks(tasks)

    def remove_task(self, task_id):
        tasks = self.load_tasks()
        if 0 <= task_id < len(tasks):
            tasks.pop(task_id)
            return self.save_tasks(tasks)
        return False