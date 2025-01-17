import tkinter as tk
from tkinter import messagebox
from calculator import Calculator

class UI:
    def __init__(self, master):
        self.master = master
        self.calculator = Calculator()
        self.create_main_window()

    def create_main_window(self):
        self.master.title("Calculation Assistant")

        self.entry = tk.Entry(self.master)
        self.entry.pack()

        self.result_display = tk.Text(self.master, height=5, width=30)
        self.result_display.pack()

        self.create_buttons()

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

        for (text, command) in operations:
            button = tk.Button(self.master, text=text, command=command)
            button.pack()

    def display_result(self, result: float):
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, str(result))

    def get_user_input(self) -> tuple:
        input_data = self.entry.get().split(',')
        return tuple(map(float, input_data))
    
    def add(self):
        a, b = self.get_user_input()
        result = self.calculator.add(a, b)
        self.display_result(result)

    def subtract(self):
        a, b = self.get_user_input()
        result = self.calculator.subtract(a, b)
        self.display_result(result)

    def multiply(self):
        a, b = self.get_user_input()
        result = self.calculator.multiply(a, b)
        self.display_result(result)

    def divide(self):
        a, b = self.get_user_input()
        try:
            result = self.calculator.divide(a, b)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def square_root(self):
        a, = self.get_user_input()
        try:
            result = self.calculator.square_root(a)
            self.display_result(result)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def exponentiate(self):
        a, b = self.get_user_input()
        result = self.calculator.exponentiate(a, b)
        self.display_result(result)

    def calculate_percentage(self):
        total, percentage = self.get_user_input()
        result = self.calculator.calculate_percentage(total, percentage)
        self.display_result(result)