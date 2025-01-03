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
        self.recipes[title] = {'ingredients': ingredients, 'instructions': instructions}
        with open(self.recipes_file, 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        return True

    def search_recipes(self, keyword: str) -> list:
        return [title for title in self.recipes if keyword.lower() in title.lower()]

    def get_recipe_details(self, title: str) -> dict:
        return self.recipes.get(title, {})

    def get_user_recipes(self, username: str) -> list:
        # This method retrieves recipes submitted by the user
        return [title for title, data in self.recipes.items() if data.get('submitted_by') == username]