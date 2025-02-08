import pytz
from datetime import datetime

class TimeConverter:
    def __init__(self):
        self.preferences = {}
        self.load_preferences()

    def load_preferences(self) -> None:
        try:
            with open('preferences.txt', 'r') as file:
                for line in file:
                    timezone, format_type = line.strip().split(':')
                    self.preferences[timezone] = format_type
        except FileNotFoundError:
            pass

    def save_preferences(self) -> None:
        with open('preferences.txt', 'w') as file:
            for timezone, format_type in self.preferences.items():
                file.write(f"{timezone}:{format_type}\n")

    def convert_time(self, input_time: str, source_tz: str, target_tz: str, format_type: str) -> str:
        try:
            source_timezone = pytz.timezone(source_tz)
            target_timezone = pytz.timezone(target_tz)
            naive_time = datetime.strptime(input_time, format_type)
            localized_time = source_timezone.localize(naive_time)
            target_time = localized_time.astimezone(target_timezone)
            return target_time.strftime(format_type)
        except Exception as e:
            return str(e)

    def validate_input(self, input_time: str) -> bool:
        try:
            datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False