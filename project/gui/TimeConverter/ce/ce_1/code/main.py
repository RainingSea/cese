import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz
from user_preferences import UserPreferences
from error_logger import ErrorLogger

class TimeConverter:
    def __init__(self, input_time: str, source_timezone: str, target_timezone: str, time_format: str):
        self.input_time = input_time
        self.source_timezone = source_timezone
        self.target_timezone = target_timezone
        self.time_format = time_format
        self.user_preferences = UserPreferences()
        self.error_logger = ErrorLogger('error_log.txt')

    def convert_time(self) -> str:
        try:
            source_tz = pytz.timezone(self.source_timezone)
            target_tz = pytz.timezone(self.target_timezone)
            naive_time = datetime.strptime(self.input_time, self.time_format)
            localized_time = source_tz.localize(naive_time)
            target_time = localized_time.astimezone(target_tz)
            return target_time.strftime(self.time_format)
        except Exception as e:
            self.log_error(str(e))
            return "Error in conversion"

    def save_preferences(self) -> None:
        preferences = {
            'source_timezone': self.source_timezone,
            'target_timezone': self.target_timezone,
            'time_format': self.time_format
        }
        self.user_preferences.save(preferences)

    def load_preferences(self) -> None:
        preferences = self.user_preferences.load()
        if preferences:
            self.source_timezone = preferences.get('source_timezone', self.source_timezone)
            self.target_timezone = preferences.get('target_timezone', self.target_timezone)
            self.time_format = preferences.get('time_format', self.time_format)

    def log_error(self, message: str) -> None:
        self.error_logger.log(message)

class TimeConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Time Converter")
        
        self.converter = TimeConverter("", "UTC", "UTC", "%Y-%m-%d %H:%M:%S")
        self.converter.load_preferences()

        self.input_time_label = tk.Label(master, text="Input Time:")
        self.input_time_label.pack()
        self.input_time_entry = tk.Entry(master)
        self.input_time_entry.pack()

        self.source_timezone_label = tk.Label(master, text="Source Timezone:")
        self.source_timezone_label.pack()
        self.source_timezone_entry = tk.Entry(master)
        self.source_timezone_entry.insert(0, self.converter.source_timezone)
        self.source_timezone_entry.pack()

        self.target_timezone_label = tk.Label(master, text="Target Timezone:")
        self.target_timezone_label.pack()
        self.target_timezone_entry = tk.Entry(master)
        self.target_timezone_entry.insert(0, self.converter.target_timezone)
        self.target_timezone_entry.pack()

        self.time_format_label = tk.Label(master, text="Time Format:")
        self.time_format_label.pack()
        self.time_format_entry = tk.Entry(master)
        self.time_format_entry.insert(0, self.converter.time_format)
        self.time_format_entry.pack()

        self.convert_button = tk.Button(master, text="Convert", command=self.convert_time)
        self.convert_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def convert_time(self):
        self.converter.input_time = self.input_time_entry.get()
        self.converter.source_timezone = self.source_timezone_entry.get()
        self.converter.target_timezone = self.target_timezone_entry.get()
        self.converter.time_format = self.time_format_entry.get()
        
        result = self.converter.convert_time()
        self.result_label.config(text=result)
        self.converter.save_preferences()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeConverterApp(root)
    root.mainloop()