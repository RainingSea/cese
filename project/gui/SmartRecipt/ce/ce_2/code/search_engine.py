class SearchEngine:
    def __init__(self):
        self.receipts = self.load_receipts()

    def load_receipts(self):
        try:
            with open('receipts.txt', 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            return []

    def add_receipt(self, date: str, merchant: str, total_amount: float) -> None:
        receipt = f"{date},{merchant},{total_amount}"
        self.receipts.append(receipt)
        with open('receipts.txt', 'a') as file:
            file.write(receipt + "\n")

    def search_receipts(self, query: str) -> list:
        results = [receipt for receipt in self.receipts if query in receipt]
        return results