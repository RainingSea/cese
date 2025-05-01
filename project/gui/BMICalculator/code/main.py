import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class BMI_Calculator:
    def __init__(self):
        self.weight = 0.0
        self.height = 0.0
        self.bmi = 0.0

    def calculate_bmi(self) -> float:
        """Calculates the BMI using the formula: BMI = weight (kg) / (height (m) * height (m))."""
        if self.height <= 0:
            raise ValueError("Height must be greater than zero.")
        return self.weight / (self.height * self.height)

    def classify_bmi(self) -> str:
        """Classifies the calculated BMI into categories: underweight, normal, overweight, and obese."""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def interpretation(self) -> str:
        """Provides an interpretation of the user's BMI based on the calculated value."""
        if self.bmi < 18.5:
            return "You are underweight. Consider consulting a healthcare provider."
        elif 18.5 <= self.bmi < 24.9:
            return "You have a normal weight. Keep up the good work!"
        elif 25 <= self.bmi < 29.9:
            return "You are overweight. Consider a balanced diet and exercise."
        else:
            return "You are obese. It's advisable to seek medical advice."

    def recommendations(self) -> str:
        """Provides recommendations for improvement based on the user's BMI category."""
        classification = self.classify_bmi()
        if classification == "Underweight":
            return "Increase your calorie intake with healthy foods."
        elif classification == "Normal":
            return "Maintain your current lifestyle."
        elif classification == "Overweight":
            return "Incorporate regular exercise into your routine."
        else:
            return "Focus on a healthy diet and consult a healthcare provider."

    def save_result(self) -> None:
        """Saves the BMI calculation results to a local text file with a timestamp."""
        with open('bmi_results.txt', 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}, {self.weight}, {self.height}, {self.bmi}, "
                       f"{self.classify_bmi()}, {self.interpretation()}, {self.recommendations()}\n")
            self.save_user_data(self.weight, self.height, self.bmi, self.classify_bmi())

    def save_user_data(self, weight: float, height: float, bmi: float, bmi_category: str) -> None:
        """Saves user data to a separate text file."""
        weight_str = f"{int(weight)}" if weight.is_integer() else f"{weight:.2f}"
        height_str = f"{int(height)}" if height.is_integer() else f"{height:.2f}"
        with open("user_data.txt", 'a') as file:
            file.write(f"{weight_str}|{height_str}|{bmi:.2f}|{bmi_category}\n")

    def validate_input(self, weight: str, height: str) -> bool:
        """Validates user input to ensure it is numeric, positive, and non-zero."""
        try:
            self.weight = float(weight)
            self.height = float(height)
            if self.weight <= 0 or self.height <= 0:
                raise ValueError("Weight and height must be positive numbers.")
            return True
        except ValueError:
            return False

    def display_error(self, message: str) -> None:
        """Displays error messages for invalid inputs in the UI."""
        messagebox.showerror("Input Error", message)

def interpret_bmi(bmi: float) -> str:
    """Interprets the BMI value."""
    return f"Your BMI is {bmi:.2f}."

def setup_gui(master: tk.Tk) -> None:
    """Sets up the GUI components for the BMI calculator."""
    tk.Label(master, text="Weight (kg):").grid(row=0, column=0)
    weight_entry = tk.Entry(master)
    weight_entry.grid(row=0, column=1)

    tk.Label(master, text="Height (m):").grid(row=1, column=0)
    height_entry = tk.Entry(master)
    height_entry.grid(row=1, column=1)

    return weight_entry, height_entry

def main() -> None:
    """Entry point of the application that initializes the GUI and handles user interactions."""
    bmi_calculator = BMI_Calculator()

    root = tk.Tk()
    root.title("BMI Calculator")

    weight_entry, height_entry = setup_gui(root)

    def calculate() -> None:
        weight = weight_entry.get()
        height = height_entry.get()
        if bmi_calculator.validate_input(weight, height):
            bmi_calculator.bmi = bmi_calculator.calculate_bmi()
            result = f"BMI: {bmi_calculator.bmi:.2f}\n" \
                     f"Classification: {bmi_calculator.classify_bmi()}\n" \
                     f"Interpretation: {bmi_calculator.interpretation()}\n" \
                     f"Recommendations: {bmi_calculator.recommendations()}"
            result_label.config(text=result)
            bmi_calculator.save_result()
        else:
            bmi_calculator.display_error("Please enter valid positive numbers for weight and height.")

    calculate_button = tk.Button(root, text="Calculate BMI", command=calculate)
    calculate_button.grid(row=2, columnspan=2)

    result_label = tk.Label(root, text="")
    result_label.grid(row=3, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()