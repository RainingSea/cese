import tkinter as tk
from tkinter import messagebox
import math

class CalculationAssistant:
    def __init__(self):
        self.result = 0.0

    def add(self, a: float, b: float) -> float:
        self.result = a + b
        return self.result

    def subtract(self, a: float, b: float) -> float:
        self.result = a - b
        return self.result

    def multiply(self, a: float, b: float) -> float:
        self.result = a * b
        return self.result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        self.result = a / b
        return self.result

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot take square root of a negative number.")
        self.result = math.sqrt(a)
        return self.result

    def exponentiate(self, base: float, exponent: float) -> float:
        self.result = base ** exponent
        return self.result

    def calculate_percentage(self, value: float, percentage: float) -> float:
        self.result = (value * percentage) / 100
        return self.result

class GUI:
    def __init__(self, master):
        self.master = master
        self.calculator = CalculationAssistant()
        self.master.title("Calculation Assistant")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.input_field = tk.Entry(self.master, width=20)
        self.input_field.grid(row=0, column=0, columnspan=4)

        self.result_display = tk.Label(self.master, text="", width=20)
        self.result_display.grid(row=1, column=0, columnspan=4)

        buttons = [
            ('+', self.on_add),
            ('-', self.on_subtract),
            ('*', self.on_multiply),
            ('/', self.on_divide),
            ('√', self.on_square_root),
            ('^', self.on_exponentiate),
            ('%', self.on_calculate_percentage)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(self.master, text=text, command=command)
            button.grid(row=2 + i // 4, column=i % 4)

    def on_add(self) -> None:
        self.perform_operation(self.calculator.add)

    def on_subtract(self) -> None:
        self.perform_operation(self.calculator.subtract)

    def on_multiply(self) -> None:
        self.perform_operation(self.calculator.multiply)

    def on_divide(self) -> None:
        self.perform_operation(self.calculator.divide)

    def on_square_root(self) -> None:
        try:
            a = float(self.input_field.get())
            result = self.calculator.square_root(a)
            self.result_display.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_exponentiate(self) -> None:
        self.perform_exponentiation()

    def on_calculate_percentage(self) -> None:
        self.perform_percentage_calculation()

    def perform_operation(self, operation) -> None:
        try:
            a, b = map(float, self.input_field.get().split())
            result = operation(a, b)
            self.result_display.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input. Please enter two numbers separated by space.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_exponentiation(self) -> None:
        try:
            base, exponent = map(float, self.input_field.get().split())
            result = self.calculator.exponentiate(base, exponent)
            self.result_display.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input. Please enter base and exponent separated by space.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_percentage_calculation(self) -> None:
        try:
            value, percentage = map(float, self.input_field.get().split())
            result = self.calculator.calculate_percentage(value, percentage)
            self.result_display.config(text=str(result))
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input. Please enter value and percentage separated by space.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()