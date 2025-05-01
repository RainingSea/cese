import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='calculations.log', level=logging.INFO, format='%(asctime)s - %(message)s')
error_logging = logging.getLogger('error')

class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot take square root of a negative number.")
        return a ** 0.5

    def exponentiate(self, base: float, exponent: float) -> float:
        return base ** exponent

    def percentage(self, part: float, whole: float) -> float:
        if whole == 0:
            raise ValueError("Whole cannot be zero for percentage calculation.")
        return (part / whole) * 100

class CalculationAssistant:
    def __init__(self, master):
        self.master = master
        self.calculator = Calculator()
        self.result_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Calculation Assistant")

        self.input_a = tk.Entry(self.master)
        self.input_a.grid(row=0, column=1)

        self.input_b = tk.Entry(self.master)
        self.input_b.grid(row=1, column=1)

        tk.Label(self.master, text="Input A:").grid(row=0, column=0)
        tk.Label(self.master, text="Input B:").grid(row=1, column=0)

        self.result_display = tk.Label(self.master, textvariable=self.result_var)
        self.result_display.grid(row=3, columnspan=2)

        tk.Button(self.master, text="Add", command=self.perform_addition).grid(row=2, column=0)
        tk.Button(self.master, text="Subtract", command=self.perform_subtraction).grid(row=2, column=1)
        tk.Button(self.master, text="Multiply", command=self.perform_multiplication).grid(row=2, column=2)
        tk.Button(self.master, text="Divide", command=self.perform_division).grid(row=2, column=3)
        tk.Button(self.master, text="Square Root", command=self.perform_square_root).grid(row=2, column=4)
        tk.Button(self.master, text="Exponentiate", command=self.perform_exponentiation).grid(row=2, column=5)
        tk.Button(self.master, text="Percentage", command=self.perform_percentage).grid(row=2, column=6)
        tk.Button(self.master, text="Clear", command=self.clear_fields).grid(row=4, columnspan=2)

    def perform_addition(self):
        self.perform_operation(self.calculator.add, "Addition")

    def perform_subtraction(self):
        self.perform_operation(self.calculator.subtract, "Subtraction")

    def perform_multiplication(self):
        self.perform_operation(self.calculator.multiply, "Multiplication")

    def perform_division(self):
        self.perform_operation(self.calculator.divide, "Division")

    def perform_square_root(self):
        try:
            a = float(self.input_a.get())
            result = self.calculator.square_root(a)
            self.display_result(result)
            logging.info(f'Square root of {a} = {result}')
        except ValueError as e:
            self.handle_error(str(e))

    def perform_exponentiation(self):
        try:
            a = float(self.input_a.get())
            b = float(self.input_b.get())
            result = self.calculator.exponentiate(a, b)
            self.display_result(result)
            logging.info(f'{a} raised to the power of {b} = {result}')
        except ValueError as e:
            self.handle_error(str(e))

    def perform_percentage(self):
        try:
            part = float(self.input_a.get())
            whole = float(self.input_b.get())
            result = self.calculator.percentage(part, whole)
            self.display_result(result)
            logging.info(f'Percentage of {part} out of {whole} = {result}%')
        except ValueError as e:
            self.handle_error(str(e))

    def perform_operation(self, operation, operation_name):
        try:
            a = float(self.input_a.get())
            b = float(self.input_b.get())
            result = operation(a, b)
            self.display_result(result)
            logging.info(f'{operation_name} of {a} and {b} = {result}')
        except ValueError as e:
            self.handle_error(str(e))

    def display_result(self, result: str):
        self.result_var.set(result)

    def handle_error(self, message: str):
        self.result_var.set(f"Error: {message}")
        error_logging.error(message)

    def clear_fields(self):
        self.input_a.delete(0, tk.END)
        self.input_b.delete(0, tk.END)
        self.result_var.set("")

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculationAssistant(root)
    app.run()