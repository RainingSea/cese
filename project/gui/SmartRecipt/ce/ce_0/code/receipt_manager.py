import os

class ReceiptManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_receipts()

    def add_receipt(self, date: str, merchant: str, total: float) -> None:
        with open(self.file_path, 'a') as file:
            file.write(f"{date},{merchant},{total}\n")

    def search_receipts(self, query: str) -> list:
        results = []
        for receipt in self.load_receipts():
            if query.lower() in receipt.lower():
                results.append(receipt)
        return results

    def load_receipts(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return file.read().strip().split('\n')