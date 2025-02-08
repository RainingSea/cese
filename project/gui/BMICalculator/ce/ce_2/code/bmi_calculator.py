class BMICalculator:
    def __init__(self, weight: float, height: float):
        self.weight = weight
        self.height = height

    def calculate_bmi(self) -> float:
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

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
            return "You are overweight. Consider a healthier lifestyle."
        else:
            return "You are obese. It is advisable to seek medical advice."

    def recommendation(self, bmi: float) -> str:
        if bmi < 18.5:
            return "Increase your caloric intake with nutritious foods."
        elif 18.5 <= bmi < 24.9:
            return "Maintain your current lifestyle."
        elif 25 <= bmi < 29.9:
            return "Engage in regular physical activity and monitor your diet."
        else:
            return "Consult a healthcare provider for a personalized plan."

    def save_data(self, weight: float, height: float, bmi: float, category: str, interpretation: str, recommendation: str):
        with open('bmi_data.txt', 'a') as file:
            file.write(f"{weight},{height},{bmi},{category},{interpretation},{recommendation}\n")