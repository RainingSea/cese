import pytz
from datetime import datetime

class TimeConverter:
    def __init__(self, input_time: str, source_timezone: str, target_timezone: str, time_format: str):
        self.input_time = input_time
        self.source_timezone = source_timezone
        self.target_timezone = target_timezone
        self.time_format = time_format

    def convert_time(self) -> str:
        source_tz = pytz.timezone(self.source_timezone)
        target_tz = pytz.timezone(self.target_timezone)

        naive_time = datetime.strptime(self.input_time, self.time_format)
        localized_time = source_tz.localize(naive_time)
        target_time = localized_time.astimezone(target_tz)

        return target_time.strftime(self.time_format)

    def load_preferences(self) -> dict:
        preferences = {}
        try:
            with open('preferences.txt', 'r') as file:
                for line in file:
                    key, value = line.strip().split('|')
                    preferences[key] = value
        except FileNotFoundError:
            pass  # File not found, return empty preferences
        return preferences

    def save_preferences(self, preferences: dict) -> None:
        with open('preferences.txt', 'w') as file:
            for key, value in preferences.items():
                file.write(f"{key}|{value}\n")