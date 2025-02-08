import tkinter as tk
from tkinter import messagebox
from bmi_calculator import BMI_Calculator

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BMI Calculator")
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.window, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = tk.Entry(self.window)
        self.weight_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Height (m):").grid(row=1, column=0)
        self.height_entry = tk.Entry(self.window)
        self.height_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.window, text="Calculate BMI", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, columnspan=2)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)

    def calculate(self) -> None:
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            calculator = BMI_Calculator(weight, height)
            bmi = calculator.calculate_bmi()
            classification = calculator.classify_bmi()
            interpretation = calculator.interpretation()
            recommendations = calculator.recommendations()
            calculator.save_results()

            result_text = f"BMI: {bmi:.2f}\nClassification: {classification}\nInterpretation: {interpretation}\nRecommendations: {recommendations}"
            self.display_results(result_text)
        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def display_results(self, result_text: str) -> None:
        self.result_label.config(text=result_text)

    def run(self) -> None:
        self.window.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.run()