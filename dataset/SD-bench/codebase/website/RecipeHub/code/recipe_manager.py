class RecipeManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.recipes = []
        self.load_recipes()

    def load_recipes(self):
        """Load recipes from the specified file."""
        try:
            with open(self.filename, 'r') as file:
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
        """Submit a new recipe and save it to the file."""
        self.recipes.append({
            'username': username,
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions
        })
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{title}|{ingredients}|{instructions}\n")
        return True

    def get_recipes(self) -> list:
        """Return a list of all submitted recipes."""
        return self.recipes

    def search_recipes(self, keyword: str) -> list:
        """Search for recipes by title keyword."""
        return [recipe for recipe in self.recipes if keyword.lower() in recipe['title'].lower()]

    def get_recipe_details(self, title: str) -> dict:
        """Get details of a specific recipe by title."""
        for recipe in self.recipes:
            if recipe['title'] == title:
                return recipe
        return {}