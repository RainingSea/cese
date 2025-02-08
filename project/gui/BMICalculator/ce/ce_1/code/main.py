import tkinter as tk
from tkinter import messagebox

class BMI_Calculator:
    def __init__(self, weight: float, height: float):
        self.weight = weight
        self.height = height
        self.bmi = 0.0
        self.classification = ""
        self.interpretation = ""
        self.recommendation = ""

    def calculate_bmi(self) -> float:
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        self.bmi = self.weight / (self.height ** 2)
        return round(self.bmi, 2)

    def classify_bmi(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def get_interpretation(self) -> str:
        if self.classification == "Underweight":
            return "You may need to gain weight for optimal health."
        elif self.classification == "Normal weight":
            return "You have a healthy weight. Keep it up!"
        elif self.classification == "Overweight":
            return "You may need to lose weight for better health."
        else:
            return "You should consider losing weight for health reasons."

    def get_recommendation(self) -> str:
        if self.classification == "Underweight":
            return "Consult a healthcare provider for advice."
        elif self.classification == "Normal weight":
            return "Maintain your current lifestyle."
        elif self.classification == "Overweight":
            return "Consider a balanced diet and regular exercise."
        else:
            return "Seek guidance from a healthcare professional."

    def store_data(self) -> None:
        with open('bmi_data.txt', 'a') as file:
            file.write(f"{self.weight},{self.height},{self.bmi},{self.classification},{self.interpretation},{self.recommendation}\n")

    def display_result(self) -> None:
        self.classification = self.classify_bmi()
        self.interpretation = self.get_interpretation()
        self.recommendation = self.get_recommendation()
        return self.bmi, self.classification, self.interpretation, self.recommendation

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BMI Calculator")
        self.calculator = None
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Height (m):").grid(row=1, column=0)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, columnspan=2)

    def calculate(self) -> None:
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            self.calculator = BMI_Calculator(weight, height)
            bmi = self.calculator.calculate_bmi()
            bmi, classification, interpretation, recommendation = self.calculator.display_result()
            self.calculator.store_data()
            self.result_label.config(text=f"BMI: {bmi}, Classification: {classification}\nInterpretation: {interpretation}\nRecommendation: {recommendation}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = UserInterface()
    app.run()