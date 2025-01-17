import tkinter as tk
from tkinter import messagebox
from calculations import CalculationAssistant

class CalculationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculation Assistant")

        self.entry = tk.Entry(root, width=30)
        self.entry.grid(row=0, column=0, columnspan=4)

        self.result_display = tk.Label(root, text="", width=30)
        self.result_display.grid(row=1, column=0, columnspan=4)

        self.create_buttons()
        self.calculator = CalculationAssistant()

    def create_buttons(self):
        operations = {
            '+': self.addition,
            '-': self.subtraction,
            '*': self.multiplication,
            '/': self.division,
            '√': self.square_root,
            '^': self.exponentiation,
            '%': self.percentage
        }

        row = 2
        col = 0
        for op, func in operations.items():
            button = tk.Button(self.root, text=op, command=func)
            button.grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def addition(self):
        self.perform_calculation(self.calculator.perform_addition, "+")

    def subtraction(self):
        self.perform_calculation(self.calculator.perform_subtraction, "-")

    def multiplication(self):
        self.perform_calculation(self.calculator.perform_multiplication, "*")

    def division(self):
        self.perform_calculation(self.calculator.perform_division, "/")

    def square_root(self):
        self.perform_single_input_calculation(self.calculator.calculate_square_root, "√")

    def exponentiation(self):
        self.perform_exponentiation()

    def percentage(self):
        self.perform_percentage()

    def perform_calculation(self, operation, symbol):
        try:
            a, b = map(float, self.entry.get().split())
            result = operation(a, b)
            self.display_result(f"{a} {symbol} {b} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_single_input_calculation(self, operation, symbol):
        try:
            a = float(self.entry.get())
            result = operation(a)
            self.display_result(f"{symbol} {a} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_exponentiation(self):
        try:
            base, exponent = map(float, self.entry.get().split())
            result = self.calculator.perform_exponentiation(base, exponent)
            self.display_result(f"{base} ^ {exponent} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_percentage(self):
        try:
            total, percentage = map(float, self.entry.get().split())
            result = self.calculator.calculate_percentage(total, percentage)
            self.display_result(f"{percentage}% of {total} = {result}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_result(self, result):
        self.result_display.config(text=result)
        operation = result.split('=')[0].strip()
        self.calculator.log_calculation(operation, float(result.split('=')[1].strip()))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculationApp(root)
    root.mainloop()