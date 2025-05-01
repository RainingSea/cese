import json

def load_expenses() -> List[dict]:
    try:
        with open('expenses.txt', 'r') as file:
            expenses = []
            for line in file:
                date, amount, category = line.strip().split('|')
                expenses.append({'date': date, 'amount': float(amount), 'category': category})
            return expenses
    except FileNotFoundError:
        return []

def load_categories() -> List[str]:
    try:
        with open('categories.txt', 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        return []