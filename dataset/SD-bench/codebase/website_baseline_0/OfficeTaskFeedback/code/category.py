class Category:
    def __init__(self):
        self.categories_file = 'categories.txt'
        self.load_categories()

    def load_categories(self):
        self.categories = []
        try:
            with open(self.categories_file, 'r') as file:
                for line in file:
                    self.categories.append(line.strip())
        except FileNotFoundError:
            self.categories = []

    def get_categories(self) -> list:
        return self.categories