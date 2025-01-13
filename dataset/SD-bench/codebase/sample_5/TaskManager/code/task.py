class Task:
    def __init__(self, username: str, description: str, due_date: str):
        self.username = username
        self.description = description
        self.due_date = due_date

    def save(self) -> None:
        with open('tasks.txt', 'a') as f:
            f.write(f"{self.username},{self.description},{self.due_date}\n")

    def remove(self) -> None:
        # This method will be implemented in DataStore
        pass