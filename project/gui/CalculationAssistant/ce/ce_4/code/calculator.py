class Calculator:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def square_root(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return a ** 0.5

    def exponentiate(self, base: float, exponent: float) -> float:
        return base ** exponent

    def calculate_percentage(self, total: float, percentage: float) -> float:
        return (total * percentage) / 100