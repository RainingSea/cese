import os
from task import Task

TASKS_FILE = "tasks.txt"
USERS_FILE = "users.txt"

def read_tasks() -> list:
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            for line in file:
                id, title, description, assigned_to, deadline, progress, priority = line.strip().split('|')
                task = Task(int(id), title, description, assigned_to, deadline, progress, priority)
                tasks.append(task)
    return tasks

def write_tasks(tasks: list) -> None:
    with open(TASKS_FILE, 'w') as file:
        for task in tasks:
            file.write(f"{task.id}|{task.title}|{task.description}|{task.assigned_to}|{task.deadline}|{task.progress}|{task.priority}\n")

def read_users() -> list:
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, role = line.strip().split('|')
                users.append((username, role))
    return users