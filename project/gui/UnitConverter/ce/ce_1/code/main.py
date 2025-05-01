import tkinter as tk
from tkinter import ttk
import os

class UnitConverter:
    def __init__(self):
        self.conversion_rates = {}
        self.load_conversion_rates()

    def load_conversion_rates(self):
        """Loads conversion rates from 'conversion_data.txt' into the conversion_rates dictionary."""
        if os.path.exists('conversion_data.txt'):
            with open('conversion_data.txt', 'r') as file:
                for line in file:
                    from_unit, to_unit, rate = line.strip().split('|')
                    if from_unit not in self.conversion_rates:
                        self.conversion_rates[from_unit] = {}
                    self.conversion_rates[from_unit][to_unit] = float(rate)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Converts a given value from one unit to another using the conversion rates."""
        if from_unit in self.conversion_rates and to_unit in self.conversion_rates[from_unit]:
            return value * self.conversion_rates[from_unit][to_unit]
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} is not defined.")

class Main:
    def __init__(self, root):
        self.converter = UnitConverter()
        self.root = root
        self.root.title("Unit Converter")
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI widgets."""
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(self.root, values=list(self.converter.conversion_rates.keys()))
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(self.root, values=[])
        self.to_unit.grid(row=2, column=1)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, column=1)

        self.convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=4, column=1)

        self.from_unit.bind("<<ComboboxSelected>>", self.update_to_unit_options)

        tk.Label(self.root, text="Value:").grid(row=0, column=0)
        tk.Label(self.root, text="From Unit:").grid(row=1, column=0)
        tk.Label(self.root, text="To Unit:").grid(row=2, column=0)
        tk.Label(self.root, text="Result:").grid(row=3, column=0)

    def update_to_unit_options(self, event):
        """Updates the options for the target unit based on the selected source unit."""
        selected_unit = self.from_unit.get()
        if selected_unit in self.converter.conversion_rates:
            self.to_unit['values'] = list(self.converter.conversion_rates[selected_unit].keys())
        else:
            self.to_unit['values'] = []

    def perform_conversion(self):
        """Handles the conversion process when the user triggers it, using the UnitConverter class."""
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = self.converter.convert(value, from_unit, to_unit)
            self.result_label.config(text=str(result))
        except ValueError as e:
            self.result_label.config(text=str(e))

    def run(self):
        """Initializes the GUI and starts the application."""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.run()