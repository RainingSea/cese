class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        users_data = self.load_users()
        if username in users_data:
            return False
        users_data[username] = password
        self.save_users(users_data)
        return True

    def login(self, username: str, password: str) -> bool:
        users_data = self.load_users()
        return users_data.get(username) == password

    def delete_account(self, username: str) -> bool:
        users_data = self.load_users()
        if username in users_data:
            del users_data[username]
            self.save_users(users_data)
            return True
        return False

    def load_users(self) -> dict:
        users_data = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users_data[username] = password
        return users_data

    def save_users(self, users_data: dict):
        with open('users.txt', 'w') as file:
            for username, password in users_data.items():
                file.write(f"{username}|{password}\n")

    def load_user_recipes(self, username: str) -> list:
        recipes_data = self.load_recipes()
        user_recipes = [title for title, details in recipes_data.items() if details['username'] == username]
        return user_recipes

    def load_recipes(self) -> dict:
        recipes_data = {}
        with open('recipes.txt', 'r') as file:
            for line in file:
                title, details = line.strip().split('|')
                ingredients, instructions = details.split(',')
                recipes_data[title] = {'ingredients': ingredients.split(','), 'instructions': instructions}
        return recipes_data