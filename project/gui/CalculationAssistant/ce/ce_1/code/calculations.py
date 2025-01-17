class CalculationAssistant:
    def perform_addition(self, a: float, b: float) -> float:
        return a + b

    def perform_subtraction(self, a: float, b: float) -> float:
        return a - b

    def perform_multiplication(self, a: float, b: float) -> float:
        return a * b

    def perform_division(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

    def calculate_square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return a ** 0.5

    def perform_exponentiation(self, base: float, exponent: float) -> float:
        return base ** exponent

    def calculate_percentage(self, total: float, percentage: float) -> float:
        return (total * percentage) / 100

    def log_calculation(self, operation: str, result: float) -> None:
        logger = CalculationLogger()
        logger.log_to_file('calculations.txt', operation, result)