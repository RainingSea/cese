class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def save_to_file(self):
        with open('recipes.txt', 'a') as file:
            file.write(f"{self.title}|{self.ingredients}|{self.instructions}\n")

class RecipeManager:
    def __init__(self, recipes_file: str = 'recipes.txt'):
        self.recipes_file = recipes_file
        self.load_recipes()

    def load_recipes(self):
        self.recipes = {}
        try:
            with open(self.recipes_file, 'r') as file:
                for line in file:
                    title, ingredients, instructions = line.strip().split('|')
                    self.recipes[title] = Recipe(title, ingredients, instructions)
        except FileNotFoundError:
            pass

    def submit_recipe(self, recipe: Recipe):
        recipe.save_to_file()
        self.recipes[recipe.title] = recipe

    def search_recipes(self, keyword: str):
        return [recipe for recipe in self.recipes.values() if keyword.lower() in recipe.title.lower()]

    def get_recipe_details(self, title: str) -> Recipe:
        return self.recipes.get(title)