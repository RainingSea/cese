import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytz
import os

class Main:
    def __init__(self):
        self.time_converter = TimeConverter()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Time Converter")

        # Source Time Zone
        self.source_tz_label = tk.Label(self.root, text="Source Time Zone:")
        self.source_tz_label.grid(column=0, row=0)
        self.source_tz = ttk.Combobox(self.root, values=pytz.all_timezones)
        self.source_tz.grid(column=1, row=0)

        # Target Time Zone
        self.target_tz_label = tk.Label(self.root, text="Target Time Zone:")
        self.target_tz_label.grid(column=0, row=1)
        self.target_tz = ttk.Combobox(self.root, values=pytz.all_timezones)
        self.target_tz.grid(column=1, row=1)

        # Time Input
        self.time_label = tk.Label(self.root, text="Enter Time (HH:MM):")
        self.time_label.grid(column=0, row=2)
        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(column=1, row=2)

        # Time Format
        self.format_label = tk.Label(self.root, text="Select Time Format:")
        self.format_label.grid(column=0, row=3)
        self.format_var = tk.StringVar(value="24-hour")
        self.radio_24 = tk.Radiobutton(self.root, text="24-hour", variable=self.format_var, value="24-hour")
        self.radio_24.grid(column=1, row=3, sticky='w')
        self.radio_12 = tk.Radiobutton(self.root, text="12-hour", variable=self.format_var, value="12-hour")
        self.radio_12.grid(column=1, row=4, sticky='w')

        # Convert Button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_time)
        self.convert_button.grid(column=0, row=5, columnspan=2)

        # Converted Time Display
        self.converted_time_label = tk.Label(self.root, text="Converted Time:")
        self.converted_time_label.grid(column=0, row=6)
        self.converted_time_display = tk.Label(self.root, text="")
        self.converted_time_display.grid(column=1, row=6)

        # Conversion History
        self.history_label = tk.Label(self.root, text="Conversion History:")
        self.history_label.grid(column=0, row=7)
        self.history_listbox = tk.Listbox(self.root)
        self.history_listbox.grid(column=0, row=8, columnspan=2)
        self.load_history()

        # Clear History Button
        self.clear_button = tk.Button(self.root, text="Clear History", command=self.clear_history)
        self.clear_button.grid(column=0, row=9, columnspan=2)

        self.root.mainloop()

    def convert_time(self):
        source_time = self.time_entry.get()
        source_timezone = self.source_tz.get()
        target_timezone = self.target_tz.get()
        time_format = self.format_var.get()

        try:
            # Convert input time to datetime object
            naive_time = datetime.strptime(source_time, "%H:%M")
            source_tz_obj = pytz.timezone(source_timezone)
            localized_time = source_tz_obj.localize(naive_time)

            # Convert to target timezone
            target_tz_obj = pytz.timezone(target_timezone)
            converted_time = localized_time.astimezone(target_tz_obj)

            # Format the converted time
            if time_format == "12-hour":
                formatted_time = converted_time.strftime("%I:%M %p")
            else:
                formatted_time = converted_time.strftime("%H:%M")

            self.converted_time_display.config(text=formatted_time)
            self.time_converter.source_time = source_time
            self.time_converter.source_timezone = source_timezone
            self.time_converter.target_timezone = target_timezone
            self.time_converter.format = time_format
            self.time_converter.save_history(formatted_time)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_history(self):
        history = self.time_converter.load_history()
        for entry in history:
            self.history_listbox.insert(tk.END, entry)

    def clear_history(self):
        self.time_converter.clear_history()
        self.history_listbox.delete(0, tk.END)

def main():
    app = Main()

if __name__ == "__main__":
    main()