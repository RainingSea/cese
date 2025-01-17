import tkinter as tk
from tkinter import ttk
from UnitConverter import UnitConverter

class GUI:
    def __init__(self, converter: UnitConverter):
        self.converter = converter
        self.root = tk.Tk()
        self.root.title("Unit Converter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(self.root, values=list(self.converter.conversion_factors.keys()))
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(self.root, values=list(self.converter.conversion_factors.keys()))
        self.to_unit.grid(row=2, column=1)

        self.convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=3, column=1)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=4, column=1)

        tk.Label(self.root, text="Value:").grid(row=0, column=0)
        tk.Label(self.root, text="From Unit:").grid(row=1, column=0)
        tk.Label(self.root, text="To Unit:").grid(row=2, column=0)

    def perform_conversion(self) -> None:
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = self.converter.convert(value, from_unit, to_unit)
            self.result_label.config(text=f"Result: {result}")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")