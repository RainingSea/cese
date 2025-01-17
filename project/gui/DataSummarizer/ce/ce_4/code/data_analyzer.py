import pandas as pd

class DataAnalyzer:
    def import_data(self, file_path: str) -> pd.DataFrame:
        """Imports data from a CSV file."""
        return pd.read_csv(file_path)

    def calculate_statistics(self, data: pd.DataFrame, selected_columns: list) -> dict:
        """Calculates statistics for the selected columns."""
        statistics = {}
        for column in selected_columns:
            if pd.api.types.is_numeric_dtype(data[column]):
                statistics[column] = self.analyze_numerical(data[column])
            else:
                statistics[column] = self.analyze_categorical(data[column])
        return statistics

    def analyze_numerical(self, data: pd.Series) -> dict:
        """Analyzes numerical data and returns mean, median, and mode."""
        return {
            'mean': data.mean(),
            'median': data.median(),
            'mode': data.mode().tolist()
        }

    def analyze_categorical(self, data: pd.Series) -> dict:
        """Analyzes categorical data and returns frequency distribution."""
        return data.value_counts().to_dict()