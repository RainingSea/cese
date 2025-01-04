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

    def submit_recipe(self, recipe: Recipe):
        recipe.save()

    def search_recipes(self, keyword: str) -> list:
        recipes = []
        with open(self.recipes_file, 'r') as f:
            for line in f:
                title, ingredients, instructions = line.strip().split('|')
                if keyword.lower() in title.lower():
                    recipes.append(Recipe(title, ingredients, instructions))
        return recipes

    def get_recipe_details(self, title: str) -> Recipe:
        with open(self.recipes_file, 'r') as f:
            for line in f:
                recipe_title, ingredients, instructions = line.strip().split('|')
                if recipe_title == title:
                    return Recipe(recipe_title, ingredients, instructions)
        return None