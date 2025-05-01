import pandas as pd

class DataFrame:
    def __init__(self):
        self.data = []

    def load_data(self, file_path: str) -> None:
        self.data = pd.read_csv(file_path).values.flatten().tolist()

    def get_data(self) -> list:
        return self.data