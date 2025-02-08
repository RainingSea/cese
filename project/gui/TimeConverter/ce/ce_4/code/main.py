import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz

class TimeConverter:
    def __init__(self, input_time: str, source_timezone: str, target_timezone: str, time_format: str):
        self.input_time = input_time
        self.source_timezone = source_timezone
        self.target_timezone = target_timezone
        self.time_format = time_format

    def convert_time(self) -> str:
        try:
            source_tz = pytz.timezone(self.source_timezone)
            target_tz = pytz.timezone(self.target_timezone)
            naive_time = datetime.strptime(self.input_time, self.time_format)
            localized_time = source_tz.localize(naive_time)
            target_time = localized_time.astimezone(target_tz)
            return target_time.strftime(self.time_format)
        except Exception as e:
            raise ValueError(f"Time conversion error: {str(e)}")

    def save_preferences(self) -> None:
        with open('user_preferences.txt', 'w') as f:
            f.write(f"{self.source_timezone}\n{self.target_timezone}\n{self.time_format}")

    def load_preferences(self) -> None:
        try:
            with open('user_preferences.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    self.source_timezone = lines[0].strip()
                    self.target_timezone = lines[1].strip()
                    self.time_format = lines[2].strip()
        except FileNotFoundError:
            pass

class UI:
    def __init__(self):
        self.converter = TimeConverter("", "", "", "%Y-%m-%d %H:%M:%S")
        self.converter.load_preferences()
        self.root = tk.Tk()
        self.root.title("Time Converter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.input_time_entry = tk.Entry(self.root)
        self.input_time_entry.pack()

        self.source_timezone_entry = tk.Entry(self.root)
        self.source_timezone_entry.pack()

        self.target_timezone_entry = tk.Entry(self.root)
        self.target_timezone_entry.pack()

        self.time_format_entry = tk.Entry(self.root)
        self.time_format_entry.pack()

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_button_clicked)
        self.convert_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

    def convert_button_clicked(self) -> None:
        self.error_label.config(text="")
        input_time = self.input_time_entry.get()
        source_timezone = self.source_timezone_entry.get()
        target_timezone = self.target_timezone_entry.get()
        time_format = self.time_format_entry.get()

        self.converter.input_time = input_time
        self.converter.source_timezone = source_timezone
        self.converter.target_timezone = target_timezone
        self.converter.time_format = time_format

        try:
            converted_time = self.converter.convert_time()
            self.result_label.config(text=f"Converted Time: {converted_time}")
            self.converter.save_preferences()
        except ValueError as e:
            self.display_error(str(e))

    def display_error(self, message: str) -> None:
        self.error_label.config(text=message)

if __name__ == "__main__":
    app = UI()
    app.root.mainloop()