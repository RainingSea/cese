class Recipe:
    def __init__(self):
        self.recipes = self.load_recipes()

    def load_recipes(self):
        recipes = []
        with open('recipes.txt', 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
        return recipes

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        with open('recipes.txt', 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        self.recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
        return True

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe['title'].lower()]

    def get_recipe_details(self, title: str) -> dict:
        for recipe in self.recipes:
            if recipe['title'] == title:
                return recipe
        return {}