import tkinter as tk
from tkinter import ttk
from UnitConverter import UnitConverter

class GUI:
    def __init__(self, converter: UnitConverter):
        self.converter = converter
        self.window = tk.Tk()
        self.create_main_window()

    def create_main_window(self):
        self.window.title("Unit Converter")
        
        self.input_value = tk.Entry(self.window)
        self.input_value.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(self.window, values=list(self.converter.units.keys()))
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(self.window, values=list(self.converter.units.keys()))
        self.to_unit.grid(row=2, column=1)

        self.convert_button = tk.Button(self.window, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=3, column=1)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=4, column=1)

        self.history_button = tk.Button(self.window, text="Show History", command=self.show_history)
        self.history_button.grid(row=5, column=1)

        tk.Label(self.window, text="Value:").grid(row=0, column=0)
        tk.Label(self.window, text="From Unit:").grid(row=1, column=0)
        tk.Label(self.window, text="To Unit:").grid(row=2, column=0)
        tk.Label(self.window, text="Result:").grid(row=4, column=0)

    def perform_conversion(self):
        value = float(self.input_value.get())
        from_unit = self.from_unit.get()
        to_unit = self.to_unit.get()
        result = self.converter.convert(value, from_unit, to_unit)
        self.update_result(result)

    def update_result(self, result: float):
        self.result_label.config(text=str(result))

    def show_history(self):
        history = self.converter.display_history()
        history_window = tk.Toplevel(self.window)
        history_window.title("Conversion History")
        history_text = tk.Text(history_window)
        history_text.pack()
        for entry in history:
            history_text.insert(tk.END, entry)