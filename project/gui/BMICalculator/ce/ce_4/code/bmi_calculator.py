class BMI_Calculator:
    def __init__(self, weight: float, height: float):
        self.weight = weight
        self.height = height
        self.bmi = 0.0

    def calculate_bmi(self) -> float:
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        self.bmi = self.weight / (self.height ** 2)
        return self.bmi

    def classify_bmi(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def interpretation(self) -> str:
        classification = self.classify_bmi()
        if classification == "Underweight":
            return "You are under the healthy weight range."
        elif classification == "Normal weight":
            return "You are within the healthy weight range."
        elif classification == "Overweight":
            return "You are above the healthy weight range."
        else:
            return "You are significantly above the healthy weight range."

    def recommendations(self) -> str:
        classification = self.classify_bmi()
        if classification == "Underweight":
            return "Consider a balanced diet to gain weight."
        elif classification == "Normal weight":
            return "Maintain your current lifestyle."
        elif classification == "Overweight":
            return "Consider a balanced diet and exercise."
        else:
            return "Seek medical advice for weight management."

    def save_results(self) -> None:
        with open('bmi_results.txt', 'a') as file:
            file.write(f"{self.weight}|{self.height}|{self.bmi}|{self.classify_bmi()}|{self.interpretation()}|{self.recommendations()}\n")