import tkinter as tk
from tkinter import messagebox
from BMI_Calculator import BMI_Calculator

class Main:
    def __init__(self) -> None:
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

        self.calculate_button = tk.Button(self.window, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(self.window, text="")
        self.result_label.grid(row=3, columnspan=2)

    def calculate_bmi(self) -> None:
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            calculator = BMI_Calculator(weight, height)
            bmi = calculator.calculate_bmi()
            category = calculator.classify_bmi(bmi)
            interpretation = calculator.interpret_bmi(bmi)
            recommendation = calculator.recommendations(category)
            calculator.save_data(weight, height, bmi, category, recommendation)

            self.result_label.config(text=f"BMI: {bmi:.2f}, Category: {category}\n{interpretation}\n{recommendation}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

    def main(self) -> None:
        self.window.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()