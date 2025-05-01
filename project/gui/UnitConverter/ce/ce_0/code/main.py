import tkinter as tk
from tkinter import ttk
from converter import Converter

class Main:
    def __init__(self, master):
        self.master = master
        self.converter = Converter()
        self.master.title("Unit Converter")

        self.create_widgets()

    def create_widgets(self):
        self.input_value = tk.Entry(self.master)
        self.input_value.pack()

        self.from_unit = ttk.Combobox(self.master, values=["meters", "kilometers", "centimeters", "millimeters", "miles", "yards", "feet"])
        self.from_unit.set("meters")
        self.from_unit.pack()

        self.to_unit = ttk.Combobox(self.master, values=["meters", "kilometers", "centimeters", "millimeters", "miles", "yards", "feet"])
        self.to_unit.set("kilometers")
        self.to_unit.pack()

        self.convert_button = tk.Button(self.master, text="Convert", command=self.perform_conversion)
        self.convert_button.pack()

        self.result_display = tk.Label(self.master, text="")
        self.result_display.pack()

    def perform_conversion(self):
        try:
            value = float(self.input_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            converted_value = self.converter.convert(value, from_unit, to_unit)
            self.result_display.config(text=f"Converted Value: {converted_value:.2f} {to_unit}")
            self.converter.save_conversion(value, from_unit, converted_value, to_unit)
        except ValueError as e:
            self.result_display.config(text=str(e))

    @staticmethod
    def main() -> str:
        root = tk.Tk()
        app = Main(root)
        root.mainloop()
        return "Application closed."

if __name__ == "__main__":
    Main.main()