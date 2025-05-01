class ReportManager:
    def generate_report(self, expenses) -> str:
        report = "Expense Report:\n"
        total_expense = 0.0
        category_summary = {}

        for expense in expenses:
            report += f"{expense.date}: {expense.amount} - {expense.category} - {expense.description}\n"
            total_expense += expense.amount
            if expense.category in category_summary:
                category_summary[expense.category] += expense.amount
            else:
                category_summary[expense.category] = expense.amount

        report += f"Total Expenses: {total_expense:.2f}\n"
        report += "Category Breakdown:\n"
        for category, amount in category_summary.items():
            report += f"{category}: {amount:.2f}\n"
        return report