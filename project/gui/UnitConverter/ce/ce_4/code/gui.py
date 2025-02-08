import tkinter as tk
from tkinter import StringVar
from conversion import UnitConverter

class GUI:
    def __init__(self, converter: UnitConverter):
        self.converter = converter
        self.root = tk.Tk()
        self.input_value = tk.Entry(self.root)
        self.from_unit = StringVar(self.root)
        self.to_unit = StringVar(self.root)
        self.result_label = tk.Label(self.root, text="")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter value:").pack()
        self.input_value.pack()
        
        tk.Label(self.root, text="From unit:").pack()
        self.from_unit.set("Select unit")
        from_unit_menu = tk.OptionMenu(self.root, self.from_unit, *self.converter.conversion_factors.keys())
        from_unit_menu.pack()
        
        tk.Label(self.root, text="To unit:").pack()
        self.to_unit.set("Select unit")
        to_unit_menu = tk.OptionMenu(self.root, self.to_unit, *self.converter.conversion_factors.keys())
        to_unit_menu.pack()
        
        convert_button = tk.Button(self.root, text="Convert", command=self.perform_conversion)
        convert_button.pack()
        
        self.result_label.pack()

    def perform_conversion(self):
        try:
            value = float(self.input_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = self.converter.convert(value, from_unit, to_unit)
            self.result_label.config(text=f"Result: {result}")
        except ValueError as e:
            self.result_label.config(text=f"Error: {str(e)}")