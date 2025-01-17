import tkinter as tk
from tkinter import messagebox
from time_converter import TimeConverter

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Converter")
        self.converter = None
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        tk.Label(self.root, text="Input Time (YYYY-MM-DD HH:MM):").grid(row=0, column=0)
        self.input_time_entry = tk.Entry(self.root)
        self.input_time_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Source Time Zone:").grid(row=1, column=0)
        self.source_timezone_entry = tk.Entry(self.root)
        self.source_timezone_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Target Time Zone:").grid(row=2, column=0)
        self.target_timezone_entry = tk.Entry(self.root)
        self.target_timezone_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Time Format:").grid(row=3, column=0)
        self.time_format_entry = tk.Entry(self.root)
        self.time_format_entry.grid(row=3, column=1)

        # Convert Button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=4, column=0, columnspan=2)

        # Result Display
        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=5, column=0, columnspan=2)

    def perform_conversion(self):
        input_time = self.input_time_entry.get()
        source_timezone = self.source_timezone_entry.get()
        target_timezone = self.target_timezone_entry.get()
        time_format = self.time_format_entry.get()

        self.converter = TimeConverter(input_time, source_timezone, target_timezone, time_format)
        try:
            result = self.converter.convert_time()
            self.display_result(result)
        except Exception as e:
            self.show_error(str(e))

    def display_result(self, result: str):
        self.result_label.config(text=f"Converted Time: {result}")

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()