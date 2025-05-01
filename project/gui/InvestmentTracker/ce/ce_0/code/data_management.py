def load_investments():
    investments = []
    try:
        with open('investments.txt', 'r') as file:
            for line in file:
                name, type_, amount, date = line.strip().split('|')
                investments.append(Investment(name, type_, float(amount), date))
    except FileNotFoundError:
        pass
    return investments

def load_categories():
    categories = []
    try:
        with open('categories.txt', 'r') as file:
            for line in file:
                name = line.strip()
                categories.append(Category(name))
    except FileNotFoundError:
        pass
    return categories