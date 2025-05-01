import tkinter as tk
from tkinter import messagebox

class BMI_Calculator:
    def __init__(self):
        self.weight = 0.0
        self.height = 0.0

    def calculate_bmi(self) -> float:
        """Calculates the BMI based on user input for weight and height."""
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        return self.weight / (self.height * self.height)

    def classify_bmi(self, bmi: float) -> str:
        """Classifies the calculated BMI into categories."""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def interpret_bmi(self, bmi: float) -> str:
        """Provides an interpretation of the user's BMI based on the calculated value."""
        if bmi < 18.5:
            return "You are underweight. It's advisable to consult a healthcare provider."
        elif 18.5 <= bmi < 24.9:
            return "You have a normal weight. Keep up the good work!"
        elif 25 <= bmi < 29.9:
            return "You are overweight. Consider a balanced diet and regular exercise."
        else:
            return "You are obese. It's important to seek guidance from a healthcare provider."

    def recommendation(self, bmi_category: str) -> str:
        """Offers recommendations for improvement based on the user's BMI category."""
        recommendations = {
            "Underweight": "Increase calorie intake with nutritious foods.",
            "Normal weight": "Maintain your current lifestyle.",
            "Overweight": "Engage in regular physical activity and monitor your diet.",
            "Obese": "Consult a healthcare provider for a personalized plan."
        }
        return recommendations.get(bmi_category, "No recommendations available.")

    def save_result(self, weight: float, height: float, bmi: float, classification: str, interpretation: str, recommendation: str) -> None:
        """Saves the user inputs and calculated results in a local text file."""
        with open('bmi_results.txt', 'a') as file:
            file.write(f"{weight},{height},{bmi},{classification},{interpretation},{recommendation}\n")

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.bmi_calculator = BMI_Calculator()

        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI components."""
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
        """Handles the BMI calculation and updates the GUI."""
        try:
            self.bmi_calculator.weight = float(self.weight_entry.get())
            self.bmi_calculator.height = float(self.height_entry.get())
            bmi = self.bmi_calculator.calculate_bmi()
            classification = self.bmi_calculator.classify_bmi(bmi)
            interpretation = self.bmi_calculator.interpret_bmi(bmi)
            recommendation = self.bmi_calculator.recommendation(classification)

            self.bmi_calculator.save_result(self.bmi_calculator.weight, self.bmi_calculator.height, bmi, classification, interpretation, recommendation)

            self.result_label.config(text=f"BMI: {bmi:.2f}, Classification: {classification}")
            messagebox.showinfo("Interpretation", interpretation + "\n" + recommendation)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()