import os

class BMI_Calculator:
    def __init__(self, weight: float, height: float):
        self.weight = weight
        self.height = height
        self.bmi = self.calculate_bmi()

    def calculate_bmi(self) -> float:
        """Calculate BMI using weight and height."""
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        return round(self.weight / (self.height ** 2), 2)

    def classify_bmi(self) -> str:
        """Classify the BMI value."""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def interpret_bmi(self) -> str:
        """Provide interpretation based on BMI classification."""
        classification = self.classify_bmi()
        interpretations = {
            "Underweight": "You are under the recommended weight range. Consider consulting a healthcare provider.",
            "Normal weight": "You are in the healthy weight range. Keep up the good work!",
            "Overweight": "You are above the recommended weight range. Consider lifestyle changes.",
            "Obesity": "You are significantly above the recommended weight range. It's advisable to seek medical advice."
        }
        return interpretations[classification]

    def recommendations(self) -> str:
        """Provide recommendations based on BMI classification."""
        recommendations = {
            "Underweight": "Increase calorie intake with nutritious foods.",
            "Normal weight": "Maintain a balanced diet and regular exercise.",
            "Overweight": "Incorporate physical activity and monitor diet.",
            "Obesity": "Seek guidance from a healthcare provider for a tailored plan."
        }
        return recommendations[self.classify_bmi()]

    def save_data(self) -> None:
        """Save user input and results to a text file."""
        with open('bmi_data.txt', 'a') as file:
            file.write(f"{self.weight}|{self.height}|{self.bmi}|{self.classify_bmi()}|{self.interpret_bmi()}|{self.recommendations()}\n")