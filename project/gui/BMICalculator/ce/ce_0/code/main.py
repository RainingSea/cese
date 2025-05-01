import tkinter as tk
from tkinter import messagebox

class BMI_Calculator:
    def __init__(self):
        self.weight = 0.0
        self.height = 0.0

    def calculate_bmi(self) -> float:
        return self.weight / (self.height * self.height)

    def classify_bmi(self) -> str:
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def interpret_bmi(self) -> str:
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "You are underweight. It's advisable to consult a healthcare provider."
        elif 18.5 <= bmi < 24.9:
            return "You have a normal weight. Keep up the good work!"
        elif 25 <= bmi < 29.9:
            return "You are overweight. Consider a balanced diet and exercise."
        else:
            return "You are obese. It's important to seek guidance from a healthcare provider."

    def recommendations(self) -> str:
        classification = self.classify_bmi()
        if classification == "Underweight":
            return "Increase your calorie intake with nutritious foods."
        elif classification == "Normal weight":
            return "Maintain your current lifestyle."
        elif classification == "Overweight":
            return "Engage in regular physical activity and monitor your diet."
        else:
            return "Consult a healthcare provider for a personalized weight loss plan."

    def save_data(self, weight: float, height: float) -> None:
        bmi = self.calculate_bmi()
        classification = self.classify_bmi()
        interpretation = self.interpret_bmi()
        recommendations = self.recommendations()

        with open('bmi_data.txt', 'a') as file:
            file.write(f"{weight}|{height}|{bmi:.2f}|{classification}|{interpretation}|{recommendations}\n")

class Main:
    def __init__(self, root):
        self.root = root
        self.bmi_calculator = BMI_Calculator()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("BMI Calculator")

        tk.Label(self.root, text="Weight (kg):").grid(row=0, column=0)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Height (m):").grid(row=1, column=0)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, columnspan=2)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            self.bmi_calculator.weight = weight
            self.bmi_calculator.height = height

            bmi = self.bmi_calculator.calculate_bmi()
            classification = self.bmi_calculator.classify_bmi()
            interpretation = self.bmi_calculator.interpret_bmi()
            recommendations = self.bmi_calculator.recommendations()

            self.bmi_calculator.save_data(weight, height)

            result_text = f"BMI: {bmi:.2f}\nClassification: {classification}\nInterpretation: {interpretation}\nRecommendations: {recommendations}"
            self.result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numbers for weight and height.")

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()