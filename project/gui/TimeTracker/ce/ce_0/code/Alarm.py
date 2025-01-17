import threading
import time

class Alarm:
    def __init__(self, time: str, message: str):
        self.time = time
        self.message = message
        self.is_triggered = False
        threading.Thread(target=self.run_alarm).start()

    def run_alarm(self):
        alarm_time = time.strptime(self.time, "%H:%M")
        while not self.is_triggered:
            current_time = time.localtime()
            if (current_time.tm_hour, current_time.tm_min) == (alarm_time.tm_hour, alarm_time.tm_min):
                self.trigger()
            time.sleep(60)  # Check every minute

    def trigger(self) -> None:
        self.is_triggered = True
        print(f"Alarm: {self.message}")