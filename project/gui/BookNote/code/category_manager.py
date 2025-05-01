class CategoryManager:
    def __init__(self):
        self.categories = []
        self.load_categories()

    def add_category(self, name: str):
        self.categories.append(name)
        self.save_categories()

    def load_categories(self) -> None:
        try:
            with open("categories.txt", "r") as file:
                for line in file:
                    self.categories.append(line.strip())
        except FileNotFoundError:
            pass

    def save_categories(self) -> None:
        with open("categories.txt", "w") as file:
            for category in self.categories:
                file.write(f"{category}\n")