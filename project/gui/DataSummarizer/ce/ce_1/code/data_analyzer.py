import pandas as pd
from typing import Any, Dict, List, Tuple

class DataAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def import_data(self, file_path: str) -> None:
        """Import data from a CSV file."""
        self.data = pd.read_csv(file_path)

    def calculate_mean(self, column: str) -> float:
        """Calculate the mean of a specified column."""
        return self.data[column].mean()

    def calculate_median(self, column: str) -> float:
        """Calculate the median of a specified column."""
        return self.data[column].median()

    def calculate_mode(self, column: str) -> Any:
        """Calculate the mode of a specified column."""
        return self.data[column].mode()[0]

    def calculate_range(self, column: str) -> Tuple[float, float]:
        """Calculate the range of a specified column."""
        return (self.data[column].min(), self.data[column].max())

    def calculate_frequency(self, column: str) -> Dict[Any, int]:
        """Calculate the frequency of unique values in a specified column."""
        return self.data[column].value_counts().to_dict()

    def calculate_distribution(self, column: str) -> Dict[float, float]:
        """Calculate the distribution of values in a specified column."""
        return self.data[column].value_counts(normalize=True).to_dict()

    def generate_summary(self, columns: List[str]) -> Dict[str, Dict[str, Any]]:
        """Generate a summary for the specified columns."""
        summary = {}
        for column in columns:
            summary[column] = {
                'mean': self.calculate_mean(column),
                'median': self.calculate_median(column),
                'mode': self.calculate_mode(column),
                'range': self.calculate_range(column),
                'frequency': self.calculate_frequency(column),
                'distribution': self.calculate_distribution(column)
            }
        return summary