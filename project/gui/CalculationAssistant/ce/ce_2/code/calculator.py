import datetime

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
            raise ValueError("Cannot take square root of a negative number.")
        return a ** 0.5

    def exponentiate(self, base: float, exponent: float) -> float:
        return base ** exponent

    def percentage(self, value: float, percent: float) -> float:
        return (value * percent) / 100

    def store_calculation(self, result: str) -> None:
        with open('calculations.txt', 'a') as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} | {result}\n")