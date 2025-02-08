from datetime import datetime

class Timer:
    def __init__(self, task_title: str, duration: float, start_time: datetime) -> None:
        self.task_title = task_title
        self.duration = duration
        self.start_time = start_time


class TimerManager:
    def __init__(self) -> None:
        self.timers = []

    def start_timer(self, task_title: str) -> None:
        start_time = datetime.now()
        self.timers.append(Timer(task_title, 0.0, start_time))

    def stop_timer(self, task_title: str) -> None:
        for timer in self.timers:
            if timer.task_title == task_title:
                timer.duration = (datetime.now() - timer.start_time).total_seconds()
                self.save_timers()
                break

    def load_timers(self) -> None:
        try:
            with open('timers.txt', 'r') as file:
                for line in file:
                    task_title, duration, start_time = line.strip().split('|')
                    self.timers.append(Timer(task_title, float(duration), datetime.fromisoformat(start_time)))
        except FileNotFoundError:
            pass

    def save_timers(self) -> None:
        with open('timers.txt', 'w') as file:
            for timer in self.timers:
                file.write(f"{timer.task_title}|{timer.duration}|{timer.start_time.isoformat()}\n")