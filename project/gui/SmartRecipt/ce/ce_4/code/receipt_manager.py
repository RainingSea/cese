class ReceiptManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.receipts = self.load_receipts()

    def add_receipt(self, date: str, merchant: str, total_amount: float) -> None:
        with open(self.file_path, 'a') as file:
            file.write(f"{date},{merchant},{total_amount}\n")
        self.receipts.append((date, merchant, total_amount))

    def search_receipts(self, date: str = "", merchant: str = "", total_amount: float = None) -> list:
        results = []
        for receipt in self.receipts:
            if (date and receipt[0] != date) or \
               (merchant and receipt[1] != merchant) or \
               (total_amount is not None and receipt[2] != total_amount):
                continue
            results.append(receipt)
        return results

    def load_receipts(self) -> list:
        receipts = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    date, merchant, total_amount = line.strip().split(',')
                    receipts.append((date, merchant, float(total_amount)))
        except FileNotFoundError:
            pass  # File not found, return empty list
        return receipts