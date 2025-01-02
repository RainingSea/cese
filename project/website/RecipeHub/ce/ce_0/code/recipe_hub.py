class RecipeHub:
    def __init__(self, users_file: str, recipes_file: str):
        self.users_file = users_file
        self.recipes_file = recipes_file
        self.users = self.load_users()
        self.recipes = self.load_recipes()

    def load_users(self):
        users = {}
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
                users[username] = password
        return users

    def load_recipes(self):
        recipes = []
        with open(self.recipes_file, 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append(Recipe(title, ingredients, instructions))
        return recipes

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def register_user(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def submit_recipe(self, recipe: Recipe) -> bool:
        with open(self.recipes_file, 'a') as file:
            file.write(recipe.to_string() + '\n')
        self.recipes.append(recipe)
        return True

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe.title.lower()]