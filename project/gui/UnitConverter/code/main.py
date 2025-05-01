import tkinter as tk
from tkinter import ttk, messagebox
import os

class Converter:
    def __init__(self):
        self.conversion_rates = {}
        self.load_conversion_rates()

    def load_conversion_rates(self):
        """Load conversion rates from a file."""
        if os.path.exists('conversion_rates.txt'):
            with open('conversion_rates.txt', 'r') as file:
                for line in file:
                    from_unit, to_unit, rate = line.strip().split('|')
                    self.conversion_rates[(from_unit, to_unit)] = float(rate)

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert value from one unit to another using the conversion rates."""
        if (from_unit, to_unit) in self.conversion_rates:
            return value * self.conversion_rates[(from_unit, to_unit)]
        elif (from_unit, to_unit) == ('celsius', 'fahrenheit'):
            return (value * 1.8) + 32
        elif (from_unit, to_unit) == ('fahrenheit', 'celsius'):
            return (value - 32) * 0.5556
        else:
            raise ValueError("Conversion rate not found.")

    def save_conversion_history(self, value: float, from_unit: str, to_unit: str, result: float):
        """Save the conversion history to a file."""
        with open('conversion_history.txt', 'a') as file:
            file.write(f"{value}|{from_unit}|{to_unit}|{result:.4f}\n")

    def get_conversion_history(self):
        """Retrieve the conversion history from the file."""
        try:
            with open('conversion_history.txt', 'r') as file:
                history = [line.strip() for line in file.readlines()]
                return history
        except FileNotFoundError:
            return []

class Main:
    def __init__(self, root):
        self.converter = Converter()
        self.root = root
        self.root.title("Unit Converter")

        self.value_entry = tk.Entry(root)
        self.value_entry.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(root, values=list(set(from_unit for from_unit, _ in self.converter.conversion_rates.keys())))
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(root, values=list(set(to_unit for _, to_unit in self.converter.conversion_rates.keys())))
        self.to_unit.grid(row=2, column=1)

        self.convert_button = tk.Button(root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(row=3, column=1)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=1)

        tk.Label(root, text="Value:").grid(row=0, column=0)
        tk.Label(root, text="From Unit:").grid(row=1, column=0)
        tk.Label(root, text="To Unit:").grid(row=2, column=0)
        tk.Label(root, text="Result:").grid(row=4, column=0)

    def perform_conversion(self):
        """Perform the unit conversion and display the result."""
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get().split('|')[0]  # Get the selected unit
            to_unit = self.to_unit.get().split('|')[0]      # Get the selected unit
            converted_value = self.converter.convert(value, from_unit, to_unit)
            self.result_label.config(text=f"{converted_value:.4f}")  # Display with precision
            self.converter.save_conversion_history(value, from_unit, to_unit, converted_value)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()