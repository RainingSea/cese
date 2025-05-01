import tkinter as tk
from tkinter import ttk, messagebox
from converter import Converter

class Main:
    def __init__(self, root):
        self.converter = Converter()
        self.root = root
        self.root.title("Unit Converter")

        self.value_entry = tk.Entry(root)
        self.value_entry.grid(row=0, column=1)

        self.from_unit = ttk.Combobox(root, values=self.converter.get_available_units())
        self.from_unit.grid(row=1, column=1)

        self.to_unit = ttk.Combobox(root, values=self.converter.get_available_units())
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
            from_unit = self.from_unit.get()  # Get the selected unit
            to_unit = self.to_unit.get()      # Get the selected unit
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