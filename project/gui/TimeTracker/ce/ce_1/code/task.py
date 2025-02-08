from datetime import datetime

class Task:
    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
        self.duration = 0.0
        self.timestamp = datetime.now()

    def update_duration(self, time: float) -> None:
        self.duration += time