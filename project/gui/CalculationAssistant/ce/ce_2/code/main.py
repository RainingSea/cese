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

        self.result_display = tk.Label(self.window, text="")
        self.result_display.grid(row=2, column=1)

        tk.Label(self.window, text="Input 1:").grid(row=0, column=0)
        tk.Label(self.window, text="Input 2:").grid(row=1, column=0)

        tk.Button(self.window, text="Add", command=self.add).grid(row=3, column=0)
        tk.Button(self.window, text="Subtract", command=self.subtract).grid(row=3, column=1)
        tk.Button(self.window, text="Multiply", command=self.multiply).grid(row=3, column=2)
        tk.Button(self.window, text="Divide", command=self.divide).grid(row=3, column=3)
        tk.Button(self.window, text="Square Root", command=self.square_root).grid(row=4, column=0)
        tk.Button(self.window, text="Exponentiate", command=self.exponentiate).grid(row=4, column=1)
        tk.Button(self.window, text="Percentage", command=self.percentage).grid(row=4, column=2)

    def main(self):
        self.window.mainloop()

    def add(self):
        result = float(self.input1.get()) + float(self.input2.get())
        self.display_result(result)

    def subtract(self):
        result = float(self.input1.get()) - float(self.input2.get())
        self.display_result(result)

    def multiply(self):
        result = float(self.input1.get()) * float(self.input2.get())
        self.display_result(result)

    def divide(self):
        try:
            result = float(self.input1.get()) / float(self.input2.get())
            self.display_result(result)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero.")

    def square_root(self):
        result = math.sqrt(float(self.input1.get()))
        self.display_result(result)

    def exponentiate(self):
        result = float(self.input1.get()) ** float(self.input2.get())
        self.display_result(result)

    def percentage(self):
        result = (float(self.input1.get()) / 100) * float(self.input2.get())
        self.display_result(result)

    def display_result(self, result):
        self.result_display.config(text=str(result))
        self.save_result(result)

    def save_result(self, result):
        with open('calculations.txt', 'a') as file:
            file.write(f"{result}\n")

if __name__ == "__main__":
    app = CalculationAssistant()
    app.main()