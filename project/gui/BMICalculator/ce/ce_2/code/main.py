import tkinter as tk
from tkinter import messagebox

class Main:
    def __init__(self, master):
        self.master = master
        master.title("BMI Calculator")

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.pack()

        self.weight_entry = tk.Entry(master)
        self.weight_entry.pack()

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.pack()

        self.height_entry = tk.Entry(master)
        self.height_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.run)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.classification_label = tk.Label(master, text="")
        self.classification_label.pack()

        self.interpretation_label = tk.Label(master, text="")
        self.interpretation_label.pack()

        self.recommendations_label = tk.Label(master, text="")
        self.recommendations_label.pack()

    def calculate_bmi(self, weight: float, height: float) -> float:
        return weight / (height * height)

    def classify_bmi(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def interpretation(self, bmi: float) -> str:
        return f"Your BMI is {bmi:.2f}."

    def recommendations(self, bmi_category: str) -> str:
        recommendations = {
            "Underweight": "Consider consulting a healthcare provider for advice on gaining weight.",
            "Normal weight": "Maintain your current lifestyle for optimal health.",
            "Overweight": "Consider a balanced diet and regular exercise.",
            "Obese": "Consult a healthcare provider for a personalized weight loss plan."
        }
        return recommendations.get(bmi_category, "No recommendations available.")

    def run(self) -> None:
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = self.calculate_bmi(weight, height)
            bmi_category = self.classify_bmi(bmi)
            interpretation_message = self.interpretation(bmi)
            recommendations_message = self.recommendations(bmi_category)

            self.result_label.config(text=f"BMI: {bmi:.2f}")
            self.classification_label.config(text=f"Classification: {bmi_category}")
            self.interpretation_label.config(text=interpretation_message)
            self.recommendations_label.config(text=recommendations_message)

            self.save_user_data(weight, height, bmi, bmi_category)

        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numbers for weight and height.")

    def save_user_data(self, weight: float, height: float, bmi: float, bmi_category: str) -> None:
        with open("user_data.txt", "a") as file:
            file.write(f"{weight}|{height}|{bmi:.2f}|{bmi_category}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()