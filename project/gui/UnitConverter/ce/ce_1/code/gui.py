import tkinter as tk
from tkinter import ttk
from unit_converter import UnitConverter

class GUI:
    def __init__(self, master: tk.Tk):
        self.converter = UnitConverter()
        self.converter.load_conversion_factors('conversion_options.txt')
        self.master = master
        self.master.title("Unit Converter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.value_label = tk.Label(self.master, text="Value:")
        self.value_label.grid(row=0, column=0)

        self.value_entry = tk.Entry(self.master)
        self.value_entry.grid(row=0, column=1)

        self.from_unit_label = tk.Label(self.master, text="From Unit:")
        self.from_unit_label.grid(row=1, column=0)

        self.from_unit_combo = ttk.Combobox(self.master)
        self.from_unit_combo['values'] = self.get_units()
        self.from_unit_combo.grid(row=1, column=1)

        self.to_unit_label = tk.Label(self.master, text="To Unit:")
        self.to_unit_label.grid(row=2, column=0)

        self.to_unit_combo = ttk.Combobox(self.master)
        self.to_unit_combo['values'] = self.get_units()
        self.to_unit_combo.grid(row=2, column=1)

        self.convert_button = tk.Button(self.master, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=3, column=0, columnspan=2)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2)

    def get_units(self):
        units = []
        for category in self.converter.conversion_factors.values():
            units.extend(category.keys())
        return list(set(units))

    def perform_conversion(self) -> None:
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit_combo.get()
            to_unit = self.to_unit_combo.get()
            result = self.converter.convert(value, from_unit, to_unit)
            self.result_label.config(text=f"Result: {result:.2f} {to_unit}")
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")