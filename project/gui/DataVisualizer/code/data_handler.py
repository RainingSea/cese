import pandas as pd
import os
from datetime import datetime

class DataHandler:
    def __init__(self):
        self.dataFrame = pd.DataFrame()

    def import_data(self, file_path: str) -> bool:
        try:
            self.dataFrame = pd.read_csv(file_path)
            if self.validate_data():
                return True
            else:
                return False
        except Exception as e:
            print(f"Error importing data: {e}")
            return False

    def save_data(self, file_name: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"{file_name}_{timestamp}.csv"
        self.dataFrame.to_csv(file_path, index=False)

    def validate_data(self) -> bool:
        return not self.dataFrame.empty