import pandas as pd
from typing import Any, Dict, Tuple

class DataAnalyzer:
    def __init__(self):
        self.data = None

    def import_data(self, file_path: str) -> None:
        """Import data from a CSV file."""
        self.data = pd.read_csv(file_path)

    def calculate_mean(self, variable: str) -> float:
        """Calculate the mean of a given variable."""
        return self.data[variable].mean()

    def calculate_median(self, variable: str) -> float:
        """Calculate the median of a given variable."""
        return self.data[variable].median()

    def calculate_mode(self, variable: str) -> Any:
        """Calculate the mode of a given variable."""
        return self.data[variable].mode()[0]

    def calculate_range(self, variable: str) -> Tuple[float, float]:
        """Calculate the range (min, max) of a given variable."""
        return (self.data[variable].min(), self.data[variable].max())

    def categorical_frequency(self, variable: str) -> Dict[str, int]:
        """Calculate the frequency of categories in a given variable."""
        return self.data[variable].value_counts().to_dict()

    def categorical_distribution(self, variable: str) -> Dict[str, float]:
        """Calculate the distribution of categories in a given variable."""
        return self.data[variable].value_counts(normalize=True).to_dict()

    def generate_summary(self, selected_vars: list) -> str:
        """Generate a summary of the selected variables."""
        summary = []
        for var in selected_vars:
            summary.append(f"Summary for {var}:")
            summary.append(f"Mean: {self.calculate_mean(var)}")
            summary.append(f"Median: {self.calculate_median(var)}")
            summary.append(f"Mode: {self.calculate_mode(var)}")
            summary.append(f"Range: {self.calculate_range(var)}")
            summary.append(f"Frequency: {self.categorical_frequency(var)}")
            summary.append(f"Distribution: {self.categorical_distribution(var)}")
            summary.append("\n")
        return "\n".join(summary)

    def save_summary(self, file_name: str, summary: str) -> None:
        """Save the summary to a text file."""
        with open(file_name, 'w') as f:
            f.write(summary)