import pytz
from datetime import datetime

class TimeConverter:
    def convert_time(self, source_time: str, source_tz: str, target_tz: str, format: str) -> str:
        self.validate_time_format(source_time, format)
        self.validate_timezone(source_tz)
        self.validate_timezone(target_tz)

        source_timezone = pytz.timezone(source_tz)
        target_timezone = pytz.timezone(target_tz)

        naive_time = self.parse_time(source_time, format)
        localized_time = source_timezone.localize(naive_time)
        target_time = localized_time.astimezone(target_timezone)

        return target_time.strftime("%H:%M" if format == "24-hour" else "%I:%M %p")

    def parse_time(self, time: str, format: str) -> datetime:
        if format == "24-hour":
            return datetime.strptime(time, "%H:%M")
        else:
            return datetime.strptime(time, "%I:%M %p")

    def validate_time_format(self, time: str, format: str):
        try:
            self.parse_time(time, format)
        except ValueError:
            raise ValueError(f"Invalid time format for {format}: {time}")

    def validate_timezone(self, timezone: str):
        if timezone not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {timezone}")

    def get_timezones(self):
        return pytz.all_timezones