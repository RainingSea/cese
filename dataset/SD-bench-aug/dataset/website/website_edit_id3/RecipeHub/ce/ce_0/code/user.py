from file_manager import FileManager

class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.file_manager = FileManager()

    def register(self, username: str, password: str) -> bool:
        users = self.file_manager.read_file('users.txt')
        for user in users:
            if user.split('|')[0] == username:
                return False  # User already exists
        users.append(f"{username}|{password}|")
        self.file_manager.write_file('users.txt', users)
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.file_manager.read_file('users.txt')
        for user in users:
            if user.split('|')[0] == username and user.split('|')[1] == password:
                return True
        return False

    def delete_account(self, username: str) -> bool:
        users = self.file_manager.read_file('users.txt')
        updated_users = [user for user in users if user.split('|')[0] != username]
        if len(updated_users) < len(users):
            self.file_manager.write_file('users.txt', updated_users)
            return True
        return False

    def fetch_user_recipes(self, username: str) -> list:
        recipes = self.file_manager.read_file('recipes.txt')
        user_recipes = [recipe for recipe in recipes if recipe.split('|')[0].startswith(username)]
        return user_recipes