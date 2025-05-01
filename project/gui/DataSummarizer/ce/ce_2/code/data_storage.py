import pandas as pd
import json

class DataAnalyzer:
    def __init__(self):
        self.numerical_data = NumericalData()
        self.categorical_data = CategoricalData()

    def import_data(self, file_path: str):
        if file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                data = json.load(file)
                if 'numerical' in data:
                    self.numerical_data.load_data(data['numerical'])
                if 'categorical' in data:
                    self.categorical_data.load_data(data['categorical'])
        else:
            raise ValueError("Unsupported file format. Please use a JSON file.")

    def calculate_mean(self) -> float:
        return self.numerical_data.calculate_mean()

    def calculate_median(self) -> float:
        return self.numerical_data.calculate_median()

    def calculate_mode(self) -> list:
        return self.numerical_data.calculate_mode()

    def calculate_range(self) -> tuple:
        return self.numerical_data.calculate_range()

    def calculate_frequency(self) -> dict:
        return self.categorical_data.calculate_frequency()

    def calculate_distribution(self) -> dict:
        return self.categorical_data.calculate_distribution()

    def generate_summary(self) -> str:
        summary = "Numerical Data Summary:\n"
        summary += f"Mean: {self.calculate_mean()}\n"
        summary += f"Median: {self.calculate_median()}\n"
        summary += f"Mode: {self.calculate_mode()}\n"
        summary += f"Range: {self.calculate_range()}\n"
        summary += "\nCategorical Data Summary:\n"
        summary += f"Frequency: {self.calculate_frequency()}\n"
        return summary

class NumericalData:
    def __init__(self):
        self.data = []

    def load_data(self, data: list):
        self.data = data

    def calculate_mean(self) -> float:
        return sum(self.data) / len(self.data) if self.data else 0

    def calculate_median(self) -> float:
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    def calculate_mode(self) -> list:
        frequency = {}
        for number in self.data:
            frequency[number] = frequency.get(number, 0) + 1
        max_freq = max(frequency.values())
        return [number for number, freq in frequency.items() if freq == max_freq]

    def calculate_range(self) -> tuple:
        return (min(self.data), max(self.data)) if self.data else (None, None)

class CategoricalData:
    def __init__(self):
        self.data = []

    def load_data(self, data: list):
        self.data = data

    def calculate_frequency(self) -> dict:
        frequency = {}
        for category in self.data:
            frequency[category] = frequency.get(category, 0) + 1
        return frequency

    def calculate_distribution(self) -> dict:
        total = len(self.data)
        frequency = self.calculate_frequency()
        distribution = {category: count / total for category, count in frequency.items()}
        return distribution