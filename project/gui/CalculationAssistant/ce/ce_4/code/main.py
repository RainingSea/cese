import tkinter as tk
from tkinter import messagebox
from CalculationAssistant import CalculationAssistant

class CalculationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculation Assistant")
        self.calculator = CalculationAssistant()

        self.create_widgets()

    def create_widgets(self):
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack()

        self.result_label = tk.Label(self.master, text="Result:")
        self.result_label.pack()

        self.result_display = tk.Label(self.master, text="")
        self.result_display.pack()

        self.create_buttons()

    def create_buttons(self):
        operations = [
            ("Add", self.add),
            ("Subtract", self.subtract),
            ("Multiply", self.multiply),
            ("Divide", self.divide),
            ("Square Root", self.square_root),
            ("Exponentiate", self.exponentiate),
            ("Percentage", self.percentage)
        ]

        for (text, command) in operations:
            button = tk.Button(self.master, text=text, command=command)
            button.pack()

    def add(self):
        self.calculate(self.calculator.perform_addition)

    def subtract(self):
        self.calculate(self.calculator.perform_subtraction)

    def multiply(self):
        self.calculate(self.calculator.perform_multiplication)

    def divide(self):
        self.calculate(self.calculator.perform_division)

    def square_root(self):
        self.calculate(self.calculator.calculate_square_root)

    def exponentiate(self):
        self.calculate(self.calculator.perform_exponentiation)

    def percentage(self):
        self.calculate(self.calculator.calculate_percentage)

    def calculate(self, operation):
        try:
            inputs = list(map(float, self.input_entry.get().split()))
            if operation in [self.calculator.perform_exponentiation, self.calculator.calculate_percentage]:
                result = operation(inputs[0], inputs[1])
            else:
                result = operation(*inputs)
            self.result_display.config(text=str(result))
            self.calculator.store_calculation(f"{self.input_entry.get()} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculationApp(root)
    root.mainloop()