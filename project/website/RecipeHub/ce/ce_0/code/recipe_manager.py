class RecipeManager:
    def __init__(self, filename):
        self.filename = filename
        self.recipes = self.load_recipes()

    def load_recipes(self):
        recipes = []
        with open(self.filename, 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append((title, ingredients, instructions))
        return recipes

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        self.recipes.append((title, ingredients, instructions))
        return True

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe[0].lower()]

    def get_recipe_details(self, title: str) -> str:
        for recipe in self.recipes:
            if recipe[0] == title:
                return f"Title: {recipe[0]}\nIngredients: {recipe[1]}\nInstructions: {recipe[2]}"
        return "Recipe not found."