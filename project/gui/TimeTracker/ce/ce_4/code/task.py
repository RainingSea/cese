class Task:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.duration = 0.0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = datetime.datetime.now()
            self.is_running = True

    def stop(self):
        if self.is_running:
            end_time = datetime.datetime.now()
            self.duration += (end_time - self.start_time).total_seconds()
            self.is_running = False