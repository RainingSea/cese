import tkinter as tk
import math

class CalculationAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculation Assistant")

        self.input1 = tk.Entry(self.root)
        self.input1.pack()

        self.input2 = tk.Entry(self.root)
        self.input2.pack()

        self.result_label = tk.Label(self.root, text="Result will be displayed here")
        self.result_label.pack()

        self.create_buttons()
        self.root.mainloop()

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

        for (text, operation) in operations:
            button = tk.Button(self.root, text=text, command=operation)
            button.pack()

    def add(self):
        result = float(self.input1.get()) + float(self.input2.get())
        self.display_result(result)
        self.log_calculation("Addition", float(self.input1.get()), float(self.input2.get()), result)

    def subtract(self):
        result = float(self.input1.get()) - float(self.input2.get())
        self.display_result(result)
        self.log_calculation("Subtraction", float(self.input1.get()), float(self.input2.get()), result)

    def multiply(self):
        result = float(self.input1.get()) * float(self.input2.get())
        self.display_result(result)
        self.log_calculation("Multiplication", float(self.input1.get()), float(self.input2.get()), result)

    def divide(self):
        try:
            result = float(self.input1.get()) / float(self.input2.get())
            self.display_result(result)
            self.log_calculation("Division", float(self.input1.get()), float(self.input2.get()), result)
        except ZeroDivisionError:
            self.result_label.config(text="Error: Division by zero")

    def square_root(self):
        result = math.sqrt(float(self.input1.get()))
        self.display_result(result)
        self.log_calculation("Square Root", float(self.input1.get()), None, result)

    def exponentiate(self):
        result = float(self.input1.get()) ** float(self.input2.get())
        self.display_result(result)
        self.log_calculation("Exponentiation", float(self.input1.get()), float(self.input2.get()), result)

    def calculate_percentage(self):
        result = (float(self.input1.get()) * float(self.input2.get())) / 100
        self.display_result(result)
        self.log_calculation("Percentage", float(self.input1.get()), float(self.input2.get()), result)

    def display_result(self, result):
        self.result_label.config(text=f"Result: {result}")

    def log_calculation(self, operation: str, input1: float, input2: float, result: float):
        with open("calculations.txt", "a") as file:
            if input2 is not None:
                file.write(f"{operation}: {input1}, {input2} -> {result}\n")
            else:
                file.write(f"{operation}: {input1} -> {result}\n")

if __name__ == "__main__":
    CalculationAssistant()