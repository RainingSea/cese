import tkinter as tk
from tkinter import ttk, messagebox
from unit_converter import UnitConverter

class GUI:
    def __init__(self, root: tk.Tk):
        self.converter = UnitConverter()
        self.converter.load_conversion_factors('conversion_units.txt')
        self.root = root
        self.root.title("Unit Converter")
        self.create_widgets()

    def create_widgets(self):
        self.value_label = tk.Label(self.root, text="Value:")
        self.value_label.grid(column=0, row=0)
        
        self.value_entry = tk.Entry(self.root)
        self.value_entry.grid(column=1, row=0)

        self.from_unit_label = tk.Label(self.root, text="From Unit:")
        self.from_unit_label.grid(column=0, row=1)

        self.from_unit_combo = ttk.Combobox(self.root)
        self.from_unit_combo['values'] = self._get_all_units()
        self.from_unit_combo.grid(column=1, row=1)

        self.to_unit_label = tk.Label(self.root, text="To Unit:")
        self.to_unit_label.grid(column=0, row=2)

        self.to_unit_combo = ttk.Combobox(self.root)
        self.to_unit_combo['values'] = self._get_all_units()
        self.to_unit_combo.grid(column=1, row=2)

        self.convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        self.convert_button.grid(column=0, row=3, columnspan=2)

        self.result_label = tk.Label(self.root, text="Result:")
        self.result_label.grid(column=0, row=4)

        self.result_value = tk.Label(self.root, text="")
        self.result_value.grid(column=1, row=4)

    def perform_conversion(self):
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit_combo.get()
            to_unit = self.to_unit_combo.get()
            result = self.converter.convert(value, from_unit, to_unit)
            self.result_value.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _get_all_units(self):
        units = set()
        for unit_type, unit_dict in self.converter.conversion_factors.items():
            units.update(unit_dict.keys())
        return list(units)

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()