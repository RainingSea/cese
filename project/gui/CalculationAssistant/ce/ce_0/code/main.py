import tkinter as tk
from tkinter import messagebox
import math

class CalculationAssistant:
    def main(self) -> str:
        self.root = tk.Tk()
        self.root.title("Calculation Assistant")

        self.input1 = tk.Entry(self.root)
        self.input1.grid(row=0, column=1)
        self.input2 = tk.Entry(self.root)
        self.input2.grid(row=1, column=1)

        tk.Label(self.root, text="Input 1").grid(row=0, column=0)
        tk.Label(self.root, text="Input 2").grid(row=1, column=0)

        self.result_display = tk.Text(self.root, height=10, width=30)
        self.result_display.grid(row=4, column=0, columnspan=2)

        self.create_buttons()
        
        self.root.mainloop()
        return "Application closed."

    def create_buttons(self):
        operations = [
            ("Add", self.add),
            ("Subtract", self.subtract),
            ("Multiply", self.multiply),
            ("Divide", self.divide),
            ("Square Root", self.square_root),
            ("Exponentiate", self.exponentiate),
            ("Percentage", self.calculate_percentage)
        ]

        for index, (label, operation) in enumerate(operations):
            button = tk.Button(self.root, text=label, command=operation)
            button.grid(row=2 + index, column=0)

    def add(self, num1: float, num2: float) -> float:
        return self.perform_operation("Addition", float(self.input1.get()), float(self.input2.get()), lambda x, y: x + y)

    def subtract(self, num1: float, num2: float) -> float:
        return self.perform_operation("Subtraction", float(self.input1.get()), float(self.input2.get()), lambda x, y: x - y)

    def multiply(self, num1: float, num2: float) -> float:
        return self.perform_operation("Multiplication", float(self.input1.get()), float(self.input2.get()), lambda x, y: x * y)

    def divide(self, num1: float, num2: float) -> float:
        return self.perform_operation("Division", float(self.input1.get()), float(self.input2.get()), lambda x, y: x / y)

    def square_root(self, num: float) -> float:
        number = float(self.input1.get())
        result = math.sqrt(number)
        self.save_calculation("Square Root", number, None, result)
        self.result_display.insert(tk.END, f"Square Root of {number} -> {result}\n")

    def exponentiate(self, base: float, exponent: float) -> float:
        return self.perform_operation("Exponentiation", float(self.input1.get()), float(self.input2.get()), lambda x, y: x ** y)

    def calculate_percentage(self, total: float, percentage: float) -> float:
        return self.perform_operation("Percentage", float(self.input1.get()), float(self.input2.get()), lambda x, y: (x * y) / 100)

    def perform_operation(self, operation: str, num1: float, num2: float, func) -> float:
        result = func(num1, num2)
        self.save_calculation(operation, num1, num2, result)
        self.result_display.insert(tk.END, f"{operation}: {num1}, {num2} -> {result}\n")
        return result

    def save_calculation(self, operation: str, input1: float, input2: float, result: float) -> None:
        with open("calculations.txt", "a") as file:
            file.write(f"{operation}: {input1}, {input2} -> {result}\n")

if __name__ == "__main__":
    app = CalculationAssistant()
    app.main()