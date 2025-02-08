import tkinter as tk
from tkinter import messagebox
from calculator import Calculator

class CalculationAssistant:
    def __init__(self, master):
        self.master = master
        master.title("Calculation Assistant")

        self.calculator = Calculator()

        self.label1 = tk.Label(master, text="Enter first number:")
        self.label1.pack()

        self.entry1 = tk.Entry(master)
        self.entry1.pack()

        self.label2 = tk.Label(master, text="Enter second number:")
        self.label2.pack()

        self.entry2 = tk.Entry(master)
        self.entry2.pack()

        self.result_label = tk.Label(master, text="Result:")
        self.result_label.pack()

        self.result_display = tk.Label(master, text="")
        self.result_display.pack()

        self.add_button = tk.Button(master, text="Add", command=self.add)
        self.add_button.pack()

        self.subtract_button = tk.Button(master, text="Subtract", command=self.subtract)
        self.subtract_button.pack()

        self.multiply_button = tk.Button(master, text="Multiply", command=self.multiply)
        self.multiply_button.pack()

        self.divide_button = tk.Button(master, text="Divide", command=self.divide)
        self.divide_button.pack()

        self.sqrt_button = tk.Button(master, text="Square Root", command=self.square_root)
        self.sqrt_button.pack()

        self.exponent_button = tk.Button(master, text="Exponentiate", command=self.exponentiate)
        self.exponent_button.pack()

        self.percentage_button = tk.Button(master, text="Percentage", command=self.percentage)
        self.percentage_button.pack()

    def add(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            result = self.calculator.add(a, b)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def subtract(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            result = self.calculator.subtract(a, b)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def multiply(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            result = self.calculator.multiply(a, b)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def divide(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            result = self.calculator.divide(a, b)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def square_root(self):
        try:
            a = float(self.entry1.get())
            result = self.calculator.square_root(a)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def exponentiate(self):
        try:
            base = float(self.entry1.get())
            exponent = float(self.entry2.get())
            result = self.calculator.exponentiate(base, exponent)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def percentage(self):
        try:
            value = float(self.entry1.get())
            percent = float(self.entry2.get())
            result = self.calculator.percentage(value, percent)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def display_result(self, result):
        self.result_display.config(text=str(result))
        self.calculator.store_calculation(str(result))

def main():
    root = tk.Tk()
    app = CalculationAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()