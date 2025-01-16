class Recipe:
    def __init__(self):
        self.recipes_file = 'recipes.txt'
        self.load_recipes()

    def load_recipes(self):
        self.recipes = []
        try:
            with open(self.recipes_file, 'r') as file:
                for line in file:
                    username, title, ingredients, instructions = line.strip().split('|')
                    self.recipes.append({
                        'username': username,
                        'title': title,
                        'ingredients': ingredients,
                        'instructions': instructions
                    })
        except FileNotFoundError:
            pass

    def submit_recipe(self, username: str, title: str, ingredients: str, instructions: str) -> bool:
        recipe_entry = f"{username}|{title}|{ingredients}|{instructions}\n"
        with open(self.recipes_file, 'a') as file:
            file.write(recipe_entry)
        self.recipes.append({
            'username': username,
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions
        })
        return True

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe['title'].lower()]

    def get_user_recipes(self, username: str) -> list:
        return [recipe for recipe in self.recipes if recipe['username'] == username]

    def get_recipe_by_id(self, recipe_id: int) -> dict:
        if 0 <= recipe_id < len(self.recipes):
            return self.recipes[recipe_id]
        return None