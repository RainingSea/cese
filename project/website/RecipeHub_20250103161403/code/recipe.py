class Recipe:
    def __init__(self):
        self.file_manager = FileManager()

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        recipes = self.file_manager.read_recipes()
        if title not in [recipe.split('|')[0] for recipe in recipes]:
            self.file_manager.write_recipe(title, ingredients, instructions)
            return True
        return False

    def search_recipes(self, keyword: str) -> list:
        recipes = self.file_manager.read_recipes()
        return [recipe for recipe in recipes if keyword.lower() in recipe.lower()]

    def get_recipe_details(self, title: str) -> dict:
        recipes = self.file_manager.read_recipes()
        for recipe in recipes:
            if recipe.split('|')[0] == title:
                return {
                    'title': recipe.split('|')[0],
                    'ingredients': recipe.split('|')[1],
                    'instructions': recipe.split('|')[2]
                }
        return {}