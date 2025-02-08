import os

class BMI_Calculator:
    def __init__(self, weight: float, height: float) -> None:
        self.weight = weight
        self.height = height

    def calculate_bmi(self) -> float:
        return self.weight / (self.height ** 2)

    def classify_bmi(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def interpret_bmi(self, bmi: float) -> str:
        if bmi < 18.5:
            return "You are underweight. Consider consulting a healthcare provider."
        elif 18.5 <= bmi < 24.9:
            return "You have a normal weight. Keep up the good work!"
        elif 25 <= bmi < 29.9:
            return "You are overweight. Consider a balanced diet and exercise."
        else:
            return "You are obese. It's advisable to seek medical advice."

    def recommendations(self, bmi_category: str) -> str:
        recommendations_dict = {
            "Underweight": "Increase calorie intake with nutritious foods.",
            "Normal weight": "Maintain a balanced diet and regular exercise.",
            "Overweight": "Focus on a healthy diet and increase physical activity.",
            "Obesity": "Seek guidance from a healthcare provider for a weight management plan."
        }
        return recommendations_dict.get(bmi_category, "No recommendations available.")

    def save_data(self, weight: float, height: float, bmi: float, category: str, recommendation: str) -> None:
        with open('bmi_data.txt', 'a') as file:
            file.write(f"{weight}|{height}|{bmi}|{category}|{recommendation}\n")