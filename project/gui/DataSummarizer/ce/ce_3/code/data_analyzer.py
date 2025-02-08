import pandas as pd

class DataAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def import_data(self, file_path: str) -> None:
        """Imports data from a CSV file into a DataFrame."""
        self.data = pd.read_csv(file_path)

    def compute_numerical_summary(self, variables: list) -> dict:
        """Computes statistical measures for numerical data."""
        summary = {}
        for var in variables:
            if var in self.data.columns:
                summary[var] = {
                    'mean': self.data[var].mean(),
                    'median': self.data[var].median(),
                    'mode': self.data[var].mode()[0],
                    'range': self.data[var].max() - self.data[var].min()
                }
        return summary

    def compute_categorical_summary(self, variables: list) -> dict:
        """Computes frequency and distribution for categorical data."""
        summary = {}
        for var in variables:
            if var in self.data.columns:
                summary[var] = self.data[var].value_counts().to_dict()
        return summary