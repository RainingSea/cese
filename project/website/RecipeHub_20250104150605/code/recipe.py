class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        # Here we can add logic to check if the recipe already exists
        return True

    def fetch_recipes(self) -> list:
        return self.read_recipes()

    def fetch_recipe_details(self, title: str) -> dict:
        recipes = self.read_recipes()
        for recipe in recipes:
            if recipe.split('|')[0] == title:
                return {
                    'title': recipe.split('|')[0],
                    'ingredients': recipe.split('|')[1],
                    'instructions': recipe.split('|')[2]
                }
        return {}

    def read_recipes(self):
        with open('recipes.txt', 'r') as f:
            return f.read().strip().split('\n')