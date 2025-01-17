import pandas as pd
from typing import Any, Dict, Tuple

class DataAnalyzer:
    def __init__(self):
        self.data = None

    def load_data(self, file_path: str) -> None:
        """Load data from a CSV file."""
        self.data = pd.read_csv(file_path)

    def calculate_mean(self, variable: str) -> float:
        """Calculate the mean of a given numerical variable."""
        return self.data[variable].mean()

    def calculate_median(self, variable: str) -> float:
        """Calculate the median of a given numerical variable."""
        return self.data[variable].median()

    def calculate_mode(self, variable: str) -> Any:
        """Calculate the mode of a given variable."""
        return self.data[variable].mode()[0]

    def calculate_range(self, variable: str) -> Tuple[float, float]:
        """Calculate the range (min, max) of a given numerical variable."""
        return (self.data[variable].min(), self.data[variable].max())

    def analyze_categorical(self, variable: str) -> Dict[str, int]:
        """Analyze a categorical variable and return frequency counts."""
        return self.data[variable].value_counts().to_dict()

    def generate_summary(self) -> str:
        """Generate a summary of the data analysis."""
        summary = self.data.describe(include='all').to_string()
        return summary