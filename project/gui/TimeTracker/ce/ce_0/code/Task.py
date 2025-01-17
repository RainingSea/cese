import time

class Task:
    def __init__(self, id: int, title: str, description: str):
        self.id = id
        self.title = title
        self.description = description
        self.duration = 0.0
        self.is_active = False

    def start(self) -> None:
        self.is_active = True
        start_time = time.time()
        while self.is_active:
            self.duration = time.time() - start_time
            time.sleep(1)  # Update every second

    def stop(self) -> None:
        self.is_active = False