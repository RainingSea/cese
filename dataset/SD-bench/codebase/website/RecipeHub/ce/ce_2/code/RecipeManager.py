from Recipe import Recipe

class RecipeManager:
    def __init__(self, recipes_file: str = 'recipes.txt'):
        self.recipes_file = recipes_file

    def load_recipes(self):
        recipes = []
        with open(self.recipes_file, 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append(Recipe(title, ingredients, instructions))
        return recipes

    def add_recipe(self, recipe: Recipe):
        recipe.save()