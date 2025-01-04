class Recipe:
    def __init__(self, username: str, title: str, ingredients: str, instructions: str):
        self.username = username
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def save(self):
        with open('recipes.txt', 'a') as f:
            f.write(f"{self.username}|{self.title}|{self.ingredients}|{self.instructions}\n")

class RecipeManager:
    def submit_recipe(self, recipe: Recipe) -> bool:
        recipe.save()
        return True

    def search_recipes(self, keyword: str) -> list:
        recipes = []
        with open('recipes.txt', 'r') as f:
            for line in f:
                if keyword in line:
                    recipes.append(line.strip().split('|'))
        return recipes

    def get_recipe_details(self, title: str) -> Recipe:
        with open('recipes.txt', 'r') as f:
            for line in f:
                recipe_data = line.strip().split('|')
                if recipe_data[1] == title:
                    return Recipe(recipe_data[0], recipe_data[1], recipe_data[2], recipe_data[3])
        return None