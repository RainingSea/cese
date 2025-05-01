import pandas as pd
import numpy as np

class DataHandler:
    def __init__(self):
        self.numerical_data_file = 'numerical_data.txt'
        self.categorical_data_file = 'categorical_data.txt'
        self.numerical_data = []
        self.categorical_data = []

    def import_data(self, file_path: str):
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                data = file.readlines()
                if "numerical" in file_path:
                    self.numerical_data = [float(line.strip()) for line in data]
                elif "categorical" in file_path:
                    self.categorical_data = [line.strip() for line in data]
                else:
                    raise ValueError("Unsupported data type.")
        else:
            raise ValueError("Only .txt files are supported.")

    def calculate_mean(self, data: list) -> float:
        return np.mean(data)

    def calculate_median(self, data: list) -> float:
        return np.median(data)

    def calculate_mode(self, data: list) -> float:
        return float(pd.Series(data).mode()[0])

    def calculate_range(self, data: list) -> tuple:
        return (min(data), max(data))

    def calculate_frequency(self, data: list) -> dict:
        return dict(pd.Series(data).value_counts())

    def calculate_distribution(self, data: list) -> dict:
        return {value: data.count(value) / len(data) for value in set(data)}

    def generate_summary(self) -> str:
        summary = "Numerical Data Summary:\n"
        if self.numerical_data:
            summary += f"Mean: {self.calculate_mean(self.numerical_data)}\n"
            summary += f"Median: {self.calculate_median(self.numerical_data)}\n"
            summary += f"Mode: {self.calculate_mode(self.numerical_data)}\n"
            summary += f"Range: {self.calculate_range(self.numerical_data)}\n"

        summary += "\nCategorical Data Summary:\n"
        if self.categorical_data:
            summary += f"Frequency: {self.calculate_frequency(self.categorical_data)}\n"
            summary += f"Distribution: {self.calculate_distribution(self.categorical_data)}\n"

        return summary

    def get_variable_names(self):
        return ['Variable1', 'Variable2', 'Variable3']  # Placeholder for actual variable names