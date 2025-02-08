import tkinter as tk
import math

class CalculationAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculation Assistant")
        self.input1 = tk.Entry(self.root)
        self.input2 = tk.Entry(self.root)
        self.result_label = tk.Label(self.root, text="")
        self.create_widgets()

    def create_widgets(self):
        self.input1.pack()
        self.input2.pack()
        
        tk.Button(self.root, text="Add", command=self.perform_addition).pack()
        tk.Button(self.root, text="Subtract", command=self.perform_subtraction).pack()
        tk.Button(self.root, text="Multiply", command=self.perform_multiplication).pack()
        tk.Button(self.root, text="Divide", command=self.perform_division).pack()
        tk.Button(self.root, text="Square Root", command=self.calculate_square_root).pack()
        tk.Button(self.root, text="Exponentiation", command=self.perform_exponentiation).pack()
        tk.Button(self.root, text="Percentage", command=self.calculate_percentage).pack()
        
        self.result_label.pack()

    def perform_addition(self):
        result = float(self.input1.get()) + float(self.input2.get())
        self.display_result("Addition", result)

    def perform_subtraction(self):
        result = float(self.input1.get()) - float(self.input2.get())
        self.display_result("Subtraction", result)

    def perform_multiplication(self):
        result = float(self.input1.get()) * float(self.input2.get())
        self.display_result("Multiplication", result)

    def perform_division(self):
        try:
            result = float(self.input1.get()) / float(self.input2.get())
            self.display_result("Division", result)
        except ZeroDivisionError:
            self.result_label.config(text="Error: Division by zero")

    def calculate_square_root(self):
        result = math.sqrt(float(self.input1.get()))
        self.display_result("Square Root", result)

    def perform_exponentiation(self):
        result = float(self.input1.get()) ** float(self.input2.get())
        self.display_result("Exponentiation", result)

    def calculate_percentage(self):
        result = (float(self.input1.get()) * float(self.input2.get())) / 100
        self.display_result("Percentage", result)

    def display_result(self, operation, result):
        self.result_label.config(text=f"{operation}: {result}")
        self.log_calculation(operation, self.input1.get(), self.input2.get(), result)

    def log_calculation(self, operation: str, input1: str, input2: str, result: str):
        with open('calculations.txt', 'a') as file:
            file.write(f"{operation}: {input1}, {input2} -> {result}\n")

if __name__ == "__main__":
    app = CalculationAssistant()
    app.root.mainloop()