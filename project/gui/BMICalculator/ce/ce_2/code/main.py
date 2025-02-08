import tkinter as tk
from tkinter import messagebox
from bmi_calculator import BMICalculator

class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BMI Calculator")
        self.create_widgets()
        self.calculator = None

    def create_widgets(self):
        tk.Label(self.window, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = tk.Entry(self.window)
        self.weight_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Height (m):").grid(row=1, column=0)
        self.height_entry = tk.Entry(self.window)
        self.height_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.window, text="Calculate BMI", command=self.calculate_button_clicked)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=3, columnspan=2)

    def calculate_button_clicked(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            self.calculator = BMICalculator(weight, height)
            bmi = self.calculator.calculate_bmi()
            category = self.calculator.classify_bmi(bmi)
            interpretation = self.calculator.interpret_bmi(bmi)
            recommendation = self.calculator.recommendation(bmi)
            self.display_results(bmi, category, interpretation, recommendation)
            self.calculator.save_data(weight, height, bmi, category, interpretation, recommendation)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def display_results(self, bmi: float, category: str, interpretation: str, recommendation: str):
        self.result_label.config(text=f"BMI: {bmi}\nCategory: {category}\nInterpretation: {interpretation}\nRecommendation: {recommendation}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = UI()
    app.run()