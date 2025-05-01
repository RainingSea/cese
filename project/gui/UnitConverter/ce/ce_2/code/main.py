import tkinter as tk
from tkinter import ttk
import os

class UnitConverter:
    def __init__(self):
        self.conversion_rates = {}

    def load_conversion_rates(self, file_path: str) -> None:
        """Loads conversion rates from a specified file into a dictionary."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'r') as file:
            for line in file:
                from_unit, to_unit, rate = line.strip().split('|')
                self.conversion_rates[(from_unit, to_unit)] = float(rate)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Converts a given value from one unit to another using the loaded conversion rates."""
        if (from_unit, to_unit) not in self.conversion_rates:
            raise ValueError(f"No conversion rate available for {from_unit} to {to_unit}.")
        
        return value * self.conversion_rates[(from_unit, to_unit)]

class GUI:
    def __init__(self, master):
        self.master = master
        self.unit_converter = UnitConverter()
        self.unit_converter.load_conversion_rates('conversion_rates.txt')
        self.create_window()

    def create_window(self) -> None:
        """Creates the main application window and initializes GUI components."""
        self.master.title("Unit Converter")

        self.input_value = tk.Entry(self.master)
        self.input_value.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(self.master, values=list(self.unit_converter.conversion_rates.keys()))
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(self.master, values=list(self.unit_converter.conversion_rates.keys()))
        self.to_unit.grid(row=2, column=1)

        self.convert_button = tk.Button(self.master, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=3, column=1)

        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_input)
        self.clear_button.grid(row=4, column=1)

        self.result_display = tk.Label(self.master, text="")
        self.result_display.grid(row=5, column=1)

    def perform_conversion(self) -> None:
        """Handles the conversion process when the user requests it."""
        try:
            value = float(self.input_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = self.unit_converter.convert(value, from_unit, to_unit)
            self.result_display.config(text=f"Result: {result:.2f}")
        except ValueError as e:
            self.result_display.config(text=f"Error: {str(e)}")

    def clear_input(self) -> None:
        """Clears the input field and output display."""
        self.input_value.delete(0, tk.END)
        self.from_unit.set('')
        self.to_unit.set('')
        self.result_display.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()