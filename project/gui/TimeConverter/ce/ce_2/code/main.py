import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytz

class TimeConverter:
    def __init__(self, source_time, source_timezone, target_timezone, format):
        self.source_time = source_time
        self.source_timezone = source_timezone
        self.target_timezone = target_timezone
        self.format = format

    def convert_time(self):
        source_tz = pytz.timezone(self.source_timezone)
        target_tz = pytz.timezone(self.target_timezone)
        naive_time = datetime.strptime(self.source_time, "%Y-%m-%d %H:%M")
        localized_time = source_tz.localize(naive_time)
        target_time = localized_time.astimezone(target_tz)
        
        if self.format == "12-hour":
            return target_time.strftime("%Y-%m-%d %I:%M %p")
        else:
            return target_time.strftime("%Y-%m-%d %H:%M")

    def save_history(self):
        with open('conversion_history.txt', 'a') as file:
            file.write(f"{self.source_time},{self.convert_time()},{self.source_timezone},{self.target_timezone},{self.format}\n")

    def clear_history(self):
        with open('conversion_history.txt', 'w') as file:
            file.truncate()

class HistoryManager:
    def __init__(self):
        self.history = []

    def load_history(self):
        try:
            with open('conversion_history.txt', 'r') as file:
                self.history = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.history = []

    def save_history(self, history):
        with open('conversion_history.txt', 'w') as file:
            for entry in history:
                file.write(f"{entry}\n")

    def clear_history(self):
        self.history = []
        with open('conversion_history.txt', 'w') as file:
            file.truncate()

class TimeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Converter")
        
        self.time_converter = TimeConverter("", "", "", "24-hour")
        self.history_manager = HistoryManager()
        self.history_manager.load_history()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Source Time (YYYY-MM-DD HH:MM):").grid(column=0, row=0)
        self.source_time_entry = ttk.Entry(self.root)
        self.source_time_entry.grid(column=1, row=0)

        ttk.Label(self.root, text="Source Time Zone:").grid(column=0, row=1)
        self.source_tz_combo = ttk.Combobox(self.root, values=pytz.all_timezones)
        self.source_tz_combo.grid(column=1, row=1)

        ttk.Label(self.root, text="Target Time Zone:").grid(column=0, row=2)
        self.target_tz_combo = ttk.Combobox(self.root, values=pytz.all_timezones)
        self.target_tz_combo.grid(column=1, row=2)

        self.format_var = tk.StringVar(value="24-hour")
        ttk.Radiobutton(self.root, text="24-hour", variable=self.format_var, value="24-hour").grid(column=0, row=3)
        ttk.Radiobutton(self.root, text="12-hour", variable=self.format_var, value="12-hour").grid(column=1, row=3)

        self.convert_button = ttk.Button(self.root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(column=0, row=4)

        self.clear_history_button = ttk.Button(self.root, text="Clear History", command=self.clear_history)
        self.clear_history_button.grid(column=1, row=4)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(column=0, row=5, columnspan=2)

        self.history_listbox = tk.Listbox(self.root)
        self.history_listbox.grid(column=0, row=6, columnspan=2)
        self.load_history_to_listbox()

    def perform_conversion(self):
        source_time = self.source_time_entry.get()
        source_timezone = self.source_tz_combo.get()
        target_timezone = self.target_tz_combo.get()
        time_format = self.format_var.get()

        if not all([source_time, source_timezone, target_timezone]):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        self.time_converter = TimeConverter(source_time, source_timezone, target_timezone, time_format)
        converted_time = self.time_converter.convert_time()
        self.result_label.config(text=f"Converted Time: {converted_time}")
        self.time_converter.save_history()
        self.load_history_to_listbox()

    def clear_history(self):
        self.history_manager.clear_history()
        self.history_listbox.delete(0, tk.END)

    def load_history_to_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history_manager.history:
            self.history_listbox.insert(tk.END, entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeConverterApp(root)
    root.mainloop()