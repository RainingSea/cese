class RecipeManager:
    def __init__(self, recipes_file: str):
        self.recipes_file = recipes_file
        self.load_recipes()

    def load_recipes(self):
        self.recipes = {}
        with open(self.recipes_file, 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                self.recipes[title] = {'ingredients': ingredients, 'instructions': instructions}

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        if title in self.recipes:
            return False
        with open(self.recipes_file, 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        self.recipes[title] = {'ingredients': ingredients, 'instructions': instructions}
        return True

    def search_recipes(self, keyword: str) -> list:
        return [title for title in self.recipes if keyword.lower() in title.lower()]

    def get_recipe_details(self, title: str) -> str:
        recipe = self.recipes.get(title)
        if recipe:
            return f"Title: {title}\nIngredients: {recipe['ingredients']}\nInstructions: {recipe['instructions']}"
        return "Recipe not found."