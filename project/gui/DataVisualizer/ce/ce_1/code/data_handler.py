import pandas as pd

class DataHandler:
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def save_data(self, data: pd.DataFrame, file_path: str) -> None:
        data.to_csv(file_path, index=False)