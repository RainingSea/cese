import tkinter as tk
from tkinter import messagebox
import math

class CalculationAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculation Assistant")
        
        self.input1 = tk.StringVar()
        self.input2 = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Input 1:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.input1).grid(row=0, column=1)
        
        tk.Label(self.root, text="Input 2:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.input2).grid(row=1, column=1)
        
        tk.Button(self.root, text="Add", command=self.perform_addition).grid(row=2, column=0)
        tk.Button(self.root, text="Subtract", command=self.perform_subtraction).grid(row=2, column=1)
        tk.Button(self.root, text="Multiply", command=self.perform_multiplication).grid(row=3, column=0)
        tk.Button(self.root, text="Divide", command=self.perform_division).grid(row=3, column=1)
        tk.Button(self.root, text="Square Root", command=self.calculate_square_root).grid(row=4, column=0)
        tk.Button(self.root, text="Exponentiate", command=self.perform_exponentiation).grid(row=4, column=1)
        tk.Button(self.root, text="Percentage", command=self.calculate_percentage).grid(row=5, column=0)
        
        self.result_display = tk.Text(self.root, height=10, width=30)
        self.result_display.grid(row=6, columnspan=2)
        
    def perform_addition(self):
        result = float(self.input1.get()) + float(self.input2.get())
        self.display_result(result)
        
    def perform_subtraction(self):
        result = float(self.input1.get()) - float(self.input2.get())
        self.display_result(result)
        
    def perform_multiplication(self):
        result = float(self.input1.get()) * float(self.input2.get())
        self.display_result(result)
        
    def perform_division(self):
        try:
            result = float(self.input1.get()) / float(self.input2.get())
            self.display_result(result)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Division by zero is not allowed.")
        
    def calculate_square_root(self):
        result = math.sqrt(float(self.input1.get()))
        self.display_result(result)
        
    def perform_exponentiation(self):
        result = float(self.input1.get()) ** float(self.input2.get())
        self.display_result(result)
        
    def calculate_percentage(self):
        result = (float(self.input1.get()) * float(self.input2.get())) / 100
        self.display_result(result)
        
    def display_result(self, result):
        self.result_display.insert(tk.END, f"Result: {result}\n")
        self.save_calculation(f"Result: {result}")
        
    def save_calculation(self, result: str):
        with open("calculations.txt", "a") as file:
            file.write(result + "\n")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CalculationAssistant()
    app.run()