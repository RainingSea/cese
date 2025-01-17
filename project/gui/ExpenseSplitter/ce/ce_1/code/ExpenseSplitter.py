class ExpenseSplitter:
    def __init__(self):
        self.expenses = []

    def add_expense(self, total: float, names: list):
        self.expenses.append((total, names))

    def calculate_shares(self) -> dict:
        shares = {}
        for total, names in self.expenses:
            share = total / len(names)
            for name in names:
                if name in shares:
                    shares[name] += share
                else:
                    shares[name] = share
        return shares

    def save_expenses(self, filename: str):
        with open(filename, 'w') as file:
            for total, names in self.expenses:
                file.write(f"{total},{','.join(names)}\n")

    def load_expenses(self, filename: str):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                total = float(parts[0])
                names = parts[1:]
                self.add_expense(total, names)