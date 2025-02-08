import pandas as pd

class DataHandler:
    def read_data(self, file_path: str) -> dict:
        """Reads data from a CSV file and returns it as a dictionary."""
        data = pd.read_csv(file_path)
        return data.to_dict(orient='list')

    def write_data(self, file_path: str, data: dict) -> None:
        """Writes the provided dictionary data to a CSV file."""
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)