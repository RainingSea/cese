import pytz
from datetime import datetime

class TimeConverter:
    def convert_time(self, source_time: str, source_tz: str, target_tz: str, format: str) -> str:
        source_timezone = pytz.timezone(source_tz)
        target_timezone = pytz.timezone(target_tz)

        naive_time = datetime.strptime(source_time, "%H:%M")
        localized_time = source_timezone.localize(naive_time)
        target_time = localized_time.astimezone(target_timezone)

        if format == "12-hour":
            return target_time.strftime("%I:%M %p")
        else:
            return target_time.strftime("%H:%M")

    def save_conversion(self, source_time: str, source_tz: str, target_tz: str, converted_time: str, format: str):
        with open("conversion_history.txt", "a") as file:
            file.write(f"{source_time}, {source_tz}, {target_tz}, {converted_time}, {format}\n")

    def load_history(self) -> list:
        try:
            with open("conversion_history.txt", "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    def clear_history(self):
        open("conversion_history.txt", "w").close()

    def get_timezones(self):
        return pytz.all_timezones