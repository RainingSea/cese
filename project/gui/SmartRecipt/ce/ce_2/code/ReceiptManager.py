import os

class ReceiptManager:
    def __init__(self, file_path='receipts'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

    def save_receipt(self, date: str, merchant: str, total_amount: float) -> None:
        filename = f"{date}_{merchant}.txt"
        with open(os.path.join(self.file_path, filename), 'w') as file:
            file.write(f"{date},{merchant},{total_amount}")

    def search_receipts(self, query: str) -> list:
        results = []
        for filename in os.listdir(self.file_path):
            if query in filename:
                with open(os.path.join(self.file_path, filename), 'r') as file:
                    results.append(file.read().strip())
        return results

    def load_receipts(self) -> list:
        receipts = []
        for filename in os.listdir(self.file_path):
            with open(os.path.join(self.file_path, filename), 'r') as file:
                receipts.append(file.read().strip())
        return receipts