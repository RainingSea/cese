def validate_expense_input(amount: str, category: str, date: str) -> bool:
    try:
        float(amount)
        if not category or not date:
            return False
        # Further date validation can be added here
        return True
    except ValueError:
        return False