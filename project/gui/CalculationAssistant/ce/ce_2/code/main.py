import tkinter as tk
from tkinter import messagebox
import math

class CalculationHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, entry: str):
        self.history.append(entry)

    def get_history(self) -> list:
        return self.history

class ResultStorage:
    def __init__(self):
        self.results = []

    def add_result(self, result: float):
        self.results.append(result)

    def get_results(self) -> list:
        return self.results

class CalculationAssistant:
    def __init__(self):
        self.input1 = ""
        self.input2 = ""
        self.operation = ""
        self.history = CalculationHistory()
        self.results = ResultStorage()

    def perform_calculation(self) -> float:
        if self.operation == "add":
            return float(self.input1) + float(self.input2)
        elif self.operation == "subtract":
            return float(self.input1) - float(self.input2)
        elif self.operation == "multiply":
            return float(self.input1) * float(self.input2)
        elif self.operation == "divide":
            return float(self.input1) / float(self.input2)
        elif self.operation == "square_root":
            return self.calculate_square_root()
        elif self.operation == "exponentiation":
            return self.calculate_exponentiation()
        elif self.operation == "percentage":
            return self.calculate_percentage()
        else:
            raise ValueError("Invalid operation")

    def calculate_square_root(self) -> float:
        return math.sqrt(float(self.input1))

    def calculate_exponentiation(self) -> float:
        return float(self.input1) ** float(self.input2)

    def calculate_percentage(self) -> float:
        return (float(self.input1) * float(self.input2)) / 100

    def store_calculation(self, data: str):
        self.history.add_entry(data)
        with open('calculations.txt', 'a') as file:
            file.write(data + '\n')

    def store_result(self, result: float):
        self.results.add_result(result)
        with open('results.txt', 'a') as file:
            file.write(str(result) + '\n')

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.assistant = CalculationAssistant()

        self.input1_entry = tk.Entry(master)
        self.input1_entry.pack()

        self.input2_entry = tk.Entry(master)
        self.input2_entry.pack()

        self.result_display = tk.Text(master, height=1, width=30)
        self.result_display.pack()

        self.create_buttons()

    def create_buttons(self):
        operations = [
            ("Add", "add"),
            ("Subtract", "subtract"),
            ("Multiply", "multiply"),
            ("Divide", "divide"),
            ("Square Root", "square_root"),
            ("Exponentiation", "exponentiation"),
            ("Percentage", "percentage"),
        ]
        for (text, operation) in operations:
            button = tk.Button(self.master, text=text, command=lambda op=operation: self.calculate(op))
            button.pack()

    def calculate(self, operation):
        self.assistant.input1 = self.input1_entry.get()
        self.assistant.input2 = self.input2_entry.get() if operation not in ["square_root"] else ""
        self.assistant.operation = operation

        try:
            result = self.assistant.perform_calculation()
            self.result_display.delete(1.0, tk.END)
            self.result_display.insert(tk.END, str(result))
            self.assistant.store_calculation(f"{self.assistant.input1} {operation} {self.assistant.input2}")
            self.assistant.store_result(result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()