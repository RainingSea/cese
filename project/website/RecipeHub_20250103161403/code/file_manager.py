class FileManager:
    def read_users(self) -> list:
        try:
            with open('users.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def write_user(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def read_recipes(self) -> list:
        try:
            with open('recipes.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def write_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        with open('recipes.txt', 'a') as f:
            f.write(f"{title}|{ingredients}|{instructions}\n")
        return True