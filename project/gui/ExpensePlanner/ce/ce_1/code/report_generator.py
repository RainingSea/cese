import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self, expense_manager, budget_manager):
        self.expense_manager = expense_manager
        self.budget_manager = budget_manager

    def generate_report(self) -> str:
        expenses = self.expense_manager.get_expenses()
        report = "Expenses Report:\n"
        total = sum(exp.amount for exp in expenses)
        
        for expense in expenses:
            report += expense.get_details() + "\n"

        report += f"Total Expenses: {total}\n"
        report += self.budget_manager.check_budget_status()
        
        self.create_pie_chart(expenses)
        return report

    def create_pie_chart(self, expenses):
        categories = {}
        for expense in expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.figure(figsize=(8, 6))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title('Expense Distribution')
        plt.show()