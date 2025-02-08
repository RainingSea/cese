from math import sqrt, pow

class CalculationAssistant:
    def __init__(self):
        self.input_value = ""
        self.result_value = ""

    def perform_addition(self, a: float, b: float) -> float:
        return a + b

    def perform_subtraction(self, a: float, b: float) -> float:
        return a - b

    def perform_multiplication(self, a: float, b: float) -> float:
        return a * b

    def perform_division(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def calculate_square_root(self, value: float) -> float:
        if value < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return sqrt(value)

    def perform_exponentiation(self, base: float, exponent: float) -> float:
        return pow(base, exponent)

    def calculate_percentage(self, total: float, percentage: float) -> float:
        return (total * percentage) / 100

    def store_calculation(self, entry: str) -> None:
        history = CalculationHistory('calculations.txt')
        history.save(entry)

    def load_calculations(self) -> list:
        history = CalculationHistory('calculations.txt')
        return history.retrieve()