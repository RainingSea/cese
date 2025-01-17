class Expense:
    def __init__(self, date: str, category: str, amount: float):
        self.date = date
        self.category = category
        self.amount = amount


class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def load_expenses(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    date, category, amount = line.strip().split(',')
                    self.expenses.append(Expense(date, category, float(amount)))
        except FileNotFoundError:
            print(f"File {file_path} not found. Starting with an empty expense list.")

    def save_expenses(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.date},{expense.category},{expense.amount}\n")

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> list[Expense]:
        return [expense for expense in self.expenses if start_date <= expense.date <= end_date]

    def get_expenses_by_category(self, category: str) -> list[Expense]:
        return [expense for expense in self.expenses if expense.category == category]