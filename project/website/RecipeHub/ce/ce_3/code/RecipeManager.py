class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def save(self):
        with open('recipes.txt', 'a') as f:
            f.write(f"{self.title}|{self.ingredients}|{self.instructions}\n")

class RecipeManager:
    def __init__(self):
        self.recipes = self.load_recipes()

    def load_recipes(self):
        recipes = []
        try:
            with open('recipes.txt', 'r') as f:
                for line in f:
                    title, ingredients, instructions = line.strip().split('|')
                    recipes.append(Recipe(title, ingredients, instructions))
        except FileNotFoundError:
            pass
        return recipes

    def submit_recipe(self, title: str, ingredients: str, instructions: str):
        new_recipe = Recipe(title, ingredients, instructions)
        new_recipe.save()
        self.recipes.append(new_recipe)

    def search_recipes(self, keyword: str):
        return [recipe for recipe in self.recipes if keyword.lower() in recipe.title.lower()]

    def get_recipe_details(self, title: str):
        for recipe in self.recipes:
            if recipe.title == title:
                return recipe
        return None