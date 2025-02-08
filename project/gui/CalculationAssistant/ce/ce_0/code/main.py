import tkinter as tk
from tkinter import messagebox
import math

class CalculationAssistant:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculation Assistant")

        self.input1 = tk.Entry(self.window)
        self.input1.grid(row=0, column=1)

        self.input2 = tk.Entry(self.window)
        self.input2.grid(row=1, column=1)

        tk.Label(self.window, text="Input 1:").grid(row=0, column=0)
        tk.Label(self.window, text="Input 2:").grid(row=1, column=0)

        self.result_display = tk.Label(self.window, text="Result will be shown here.")
        self.result_display.grid(row=3, columnspan=2)

        tk.Button(self.window, text="Add", command=self.add).grid(row=2, column=0)
        tk.Button(self.window, text="Subtract", command=self.subtract).grid(row=2, column=1)
        tk.Button(self.window, text="Multiply", command=self.multiply).grid(row=2, column=2)
        tk.Button(self.window, text="Divide", command=self.divide).grid(row=2, column=3)
        tk.Button(self.window, text="Square Root", command=self.square_root).grid(row=4, column=0)
        tk.Button(self.window, text="Exponentiate", command=self.exponentiate).grid(row=4, column=1)
        tk.Button(self.window, text="Percentage", command=self.calculate_percentage).grid(row=4, column=2)

        self.window.mainloop()

    def add(self):
        result = self._calculate(float(self.input1.get()), float(self.input2.get()), '+')
        self.result_display.config(text=f"Result: {result}")

    def subtract(self):
        result = self._calculate(float(self.input1.get()), float(self.input2.get()), '-')
        self.result_display.config(text=f"Result: {result}")

    def multiply(self):
        result = self._calculate(float(self.input1.get()), float(self.input2.get()), '*')
        self.result_display.config(text=f"Result: {result}")

    def divide(self):
        try:
            result = self._calculate(float(self.input1.get()), float(self.input2.get()), '/')
            self.result_display.config(text=f"Result: {result}")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero.")

    def square_root(self):
        result = math.sqrt(float(self.input1.get()))
        self.result_display.config(text=f"Result: {result}")

    def exponentiate(self):
        result = self._calculate(float(self.input1.get()), float(self.input2.get()), '**')
        self.result_display.config(text=f"Result: {result}")

    def calculate_percentage(self):
        result = (float(self.input1.get()) * float(self.input2.get())) / 100
        self.result_display.config(text=f"Result: {result}")

    def _calculate(self, input1, input2, operation):
        if operation == '+':
            result = input1 + input2
        elif operation == '-':
            result = input1 - input2
        elif operation == '*':
            result = input1 * input2
        elif operation == '/':
            result = input1 / input2
        elif operation == '**':
            result = input1 ** input2
        else:
            raise ValueError("Invalid operation")
        
        self.log_calculation(operation, input1, input2, result)
        return result

    def log_calculation(self, operation: str, input1: float, input2: float, result: float):
        with open('calculations.txt', 'a') as file:
            file.write(f"{operation}: {input1}, {input2} -> {result}\n")

if __name__ == "__main__":
    CalculationAssistant()