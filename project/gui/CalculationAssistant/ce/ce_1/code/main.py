import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class CalculationAssistant:
    def __init__(self):
        self.result = 0.0

    def perform_addition(self, a: float, b: float) -> float:
        self.result = a + b
        self.log_calculation("Addition", self.result)
        return self.result

    def perform_subtraction(self, a: float, b: float) -> float:
        self.result = a - b
        self.log_calculation("Subtraction", self.result)
        return self.result

    def perform_multiplication(self, a: float, b: float) -> float:
        self.result = a * b
        self.log_calculation("Multiplication", self.result)
        return self.result

    def perform_division(self, a: float, b: float) -> float:
        if b == 0:
            messagebox.showerror("Error", "Division by zero is not allowed.")
            return None
        self.result = a / b
        self.log_calculation("Division", self.result)
        return self.result

    def calculate_square_root(self, a: float) -> float:
        if a < 0:
            messagebox.showerror("Error", "Cannot calculate square root of a negative number.")
            return None
        self.result = a ** 0.5
        self.log_calculation("Square Root", self.result)
        return self.result

    def perform_exponentiation(self, base: float, exponent: float) -> float:
        self.result = base ** exponent
        self.log_calculation("Exponentiation", self.result)
        return self.result

    def calculate_percentage(self, total: float, percentage: float) -> float:
        self.result = (total * percentage) / 100
        self.log_calculation("Percentage", self.result)
        return self.result

    def log_calculation(self, operation: str, result: float) -> None:
        with open("calculations.log", "a") as log_file:
            log_file.write(f"{datetime.now()}: {operation} = {result}\n")

class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculation Assistant")
        self.calculator = CalculationAssistant()
        self.create_main_window()

    def create_main_window(self) -> None:
        self.input_a = tk.Entry(self.master)
        self.input_b = tk.Entry(self.master)
        self.result_display = tk.Label(self.master, text="Result: ")

        self.input_a.grid(row=0, column=0)
        self.input_b.grid(row=0, column=1)
        self.result_display.grid(row=1, column=0, columnspan=2)

        self.setup_buttons()

    def setup_buttons(self) -> None:
        operations = [
            ("Add", self.calculator.perform_addition),
            ("Subtract", self.calculator.perform_subtraction),
            ("Multiply", self.calculator.perform_multiplication),
            ("Divide", self.calculator.perform_division),
            ("Square Root", self.calculator.calculate_square_root),
            ("Exponentiate", self.calculator.perform_exponentiation),
            ("Percentage", self.calculator.calculate_percentage),
        ]

        for i, (text, operation) in enumerate(operations):
            button = tk.Button(self.master, text=text, command=lambda op=operation: self.calculate(op))
            button.grid(row=2, column=i)

    def calculate(self, operation) -> None:
        try:
            a = float(self.input_a.get())
            b = float(self.input_b.get())
            if operation in [self.calculator.perform_addition, self.calculator.perform_subtraction,
                             self.calculator.perform_multiplication, self.calculator.perform_division,
                             self.calculator.perform_exponentiation, self.calculator.calculate_percentage]:
                result = operation(a, b)
            elif operation == self.calculator.calculate_square_root:
                result = operation(a)
            else:
                result = None

            if result is not None:
                self.display_result(result)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers only.")

    def display_result(self, result: float) -> None:
        self.result_display.config(text=f"Result: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()