import pytz
from datetime import datetime

class TimeConverter:
    def __init__(self, input_time: str, source_timezone: str, target_timezone: str, time_format: str):
        self.input_time = input_time
        self.source_timezone = source_timezone
        self.target_timezone = target_timezone
        self.time_format = time_format

    def convert_time(self) -> str:
        # Parse the input time
        local_tz = pytz.timezone(self.source_timezone)
        naive_time = datetime.strptime(self.input_time, "%Y-%m-%d %H:%M")
        local_time = local_tz.localize(naive_time)

        # Convert to target timezone
        target_tz = pytz.timezone(self.target_timezone)
        target_time = local_time.astimezone(target_tz)

        # Format the output time
        if self.time_format == "12-hour":
            return target_time.strftime("%Y-%m-%d %I:%M %p")
        else:
            return target_time.strftime("%Y-%m-%d %H:%M")

    def load_preferences(self) -> dict:
        preferences = {}
        try:
            with open('preferences.txt', 'r') as file:
                for line in file:
                    key, value = line.strip().split('|')
                    preferences[key] = value
        except FileNotFoundError:
            return preferences
        return preferences

    def save_preferences(self, preferences: dict):
        with open('preferences.txt', 'w') as file:
            for key, value in preferences.items():
                file.write(f"{key}|{value}\n")