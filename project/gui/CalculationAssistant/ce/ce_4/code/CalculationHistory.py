import os

class CalculationHistory:
    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w') as f:
                pass  # Create the file if it doesn't exist

    def save(self, entry: str) -> None:
        with open(self.file_name, 'a') as f:
            f.write(entry + '\n')

    def retrieve(self) -> list:
        with open(self.file_name, 'r') as f:
            return f.readlines()