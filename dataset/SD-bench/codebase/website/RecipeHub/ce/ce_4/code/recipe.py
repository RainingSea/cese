class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str, username: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.username = username

    def save(self):
        with open('recipes.txt', 'a') as file:
            file.write(f'{self.title},{self.ingredients},{self.instructions},{self.username}\n')