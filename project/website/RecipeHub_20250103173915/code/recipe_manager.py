class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def save(self):
        with open('recipes.txt', 'a') as f:
            f.write(f"{self.title}|{self.ingredients}|{self.instructions}\n")


class RecipeManager:
    def __init__(self, recipes_file: str):
        self.recipes_file = recipes_file

    def load_recipes(self):
        recipes = []
        with open(self.recipes_file, 'r') as f:
            for line in f:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append(Recipe(title, ingredients, instructions))
        return recipes

    def add_recipe(self, recipe: Recipe):
        recipe.save()

    def search_recipes(self, keyword: str):
        recipes = self.load_recipes()
        return [recipe for recipe in recipes if keyword.lower() in recipe.title.lower()]