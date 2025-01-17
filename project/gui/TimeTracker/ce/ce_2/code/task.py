class Task:
    def __init__(self, id: int, title: str, description: str) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.timer = 0
        self.alarm = ""

    def set_timer(self, duration: int) -> None:
        self.timer = duration

    def set_alarm(self, time: str) -> None:
        self.alarm = time