import tkinter as tk
from tkinter import messagebox
from time_converter import TimeConverter

class GUI:
    def __init__(self, converter: TimeConverter):
        self.converter = converter
        self.root = tk.Tk()
        self.root.title("Time Converter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.input_time_label = tk.Label(self.root, text="Input Time (YYYY-MM-DD HH:MM:SS):")
        self.input_time_label.pack()
        self.input_time_entry = tk.Entry(self.root)
        self.input_time_entry.pack()

        self.source_tz_label = tk.Label(self.root, text="Source Time Zone:")
        self.source_tz_label.pack()
        self.source_tz_entry = tk.Entry(self.root)
        self.source_tz_entry.pack()

        self.target_tz_label = tk.Label(self.root, text="Target Time Zone:")
        self.target_tz_label.pack()
        self.target_tz_entry = tk.Entry(self.root)
        self.target_tz_entry.pack()

        self.format_label = tk.Label(self.root, text="Time Format (e.g., %Y-%m-%d %H:%M:%S):")
        self.format_label.pack()
        self.format_entry = tk.Entry(self.root)
        self.format_entry.pack()

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_button_clicked)
        self.convert_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def convert_button_clicked(self) -> None:
        input_time = self.input_time_entry.get()
        source_tz = self.source_tz_entry.get()
        target_tz = self.target_tz_entry.get()
        format_type = self.format_entry.get()

        if not self.converter.validate_input(input_time):
            messagebox.showerror("Invalid Input", "Please enter a valid time format.")
            return

        result = self.converter.convert_time(input_time, source_tz, target_tz, format_type)
        self.result_label.config(text=result)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    converter = TimeConverter()
    app = GUI(converter)
    app.run()