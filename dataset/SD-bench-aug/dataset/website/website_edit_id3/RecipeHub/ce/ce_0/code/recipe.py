from file_manager import FileManager

class Recipe:
    def __init__(self):
        self.title = ""
        self.ingredients = []
        self.instructions = ""
        self.file_manager = FileManager()

    def submit_recipe(self, title: str, ingredients: list, instructions: str) -> bool:
        recipes = self.file_manager.read_file('recipes.txt')
        recipes.append(f"{title}|{','.join(ingredients)}|{instructions}")
        self.file_manager.write_file('recipes.txt', recipes)
        return True

    def fetch_recipes(self) -> list:
        return self.file_manager.read_file('recipes.txt')

    def fetch_recipe_details(self, title: str) -> dict:
        recipes = self.file_manager.read_file('recipes.txt')
        for recipe in recipes:
            if recipe.split('|')[0] == title:
                ingredients = recipe.split('|')[1].split(',')
                instructions = recipe.split('|')[2]
                return {'title': title, 'ingredients': ingredients, 'instructions': instructions}
        return {}