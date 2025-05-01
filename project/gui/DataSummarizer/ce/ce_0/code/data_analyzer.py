import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self):
        self.numerical_data = []
        self.categorical_data = {}

    def import_data(self, file_path: str) -> None:
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                data = file.readlines()
                self.numerical_data = [float(x.strip()) for x in data if x.strip().replace('.', '', 1).isdigit()]
                self.categorical_data = {line.split('|')[0]: int(line.split('|')[1]) for line in data if '|' in line}

    def calculate_mean(self) -> float:
        return np.mean(self.numerical_data)

    def calculate_median(self) -> float:
        return np.median(self.numerical_data)

    def calculate_mode(self) -> float:
        return float(pd.Series(self.numerical_data).mode())

    def calculate_range(self) -> float:
        return np.max(self.numerical_data) - np.min(self.numerical_data)

    def calculate_frequency(self) -> dict:
        return self.categorical_data

    def calculate_distribution(self) -> dict:
        total = sum(self.categorical_data.values())
        return {key: value / total for key, value in self.categorical_data.items()}

    def generate_summary(self) -> str:
        mean = self.calculate_mean()
        median = self.calculate_median()
        mode = self.calculate_mode()
        data_range = self.calculate_range()
        frequency = self.calculate_frequency()
        distribution = self.calculate_distribution()

        summary = (
            f"Mean: {mean}\n"
            f"Median: {median}\n"
            f"Mode: {mode}\n"
            f"Range: {data_range}\n"
            f"Frequency: {frequency}\n"
            f"Distribution: {distribution}"
        )
        return summary