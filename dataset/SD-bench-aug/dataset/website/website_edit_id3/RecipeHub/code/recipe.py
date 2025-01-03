class Recipe:
    def __init__(self, title: str, ingredients: list, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def submit_recipe(self, title: str, ingredients: list, instructions: str) -> bool:
        recipes_data = self.load_recipes()
        if title in recipes_data:
            return False
        recipes_data[title] = {'ingredients': ingredients, 'instructions': instructions}
        self.save_recipes(recipes_data)
        return True

    def fetch_recipes(self) -> list:
        recipes_data = self.load_recipes()
        return list(recipes_data.keys())

    def fetch_recipe_details(self, title: str) -> dict:
        recipes_data = self.load_recipes()
        return recipes_data.get(title, {})

    def load_recipes(self) -> dict:
        recipes_data = {}
        with open('recipes.txt', 'r') as file:
            for line in file:
                title, details = line.strip().split('|')
                ingredients, instructions = details.split(',')
                recipes_data[title] = {'ingredients': ingredients.split(','), 'instructions': instructions}
        return recipes_data

    def save_recipes(self, recipes_data: dict):
        with open('recipes.txt', 'w') as file:
            for title, details in recipes_data.items():
                ingredients = ','.join(details['ingredients'])
                instructions = details['instructions']
                file.write(f"{title}|{ingredients},{instructions}\n")