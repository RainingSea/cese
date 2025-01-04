class Recipe:
    def __init__(self):
        self.title = ""
        self.ingredients = ""
        self.instructions = ""

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        with open('recipes.txt', 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        return True

    def fetch_recipes(self) -> list:
        return recipes

    def fetch_recipe_details(self, title: str) -> dict:
        for recipe in recipes:
            if recipe['title'] == title:
                return recipe
        return {}