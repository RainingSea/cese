class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

class DataManager:
    def register(self, username: str, password: str):
        if User.load(username) is None:  # Check if user already exists
            new_user = User(username, password)
            new_user.save()
            return True
        return False

    def login(self, username: str, password: str):
        user = User.load(username)
        if user and user.password == password:
            return True
        return False

    def load_tips(self):
        tips = []
        try:
            with open('tips.txt', 'r') as f:
                for line in f:
                    tips.append(line.strip())
        except FileNotFoundError:
            print("Tips file not found.")
        return tips

    def save_tip(self, username: str, tip: str):
        with open('tips.txt', 'a') as f:
            f.write(f"{username}|{tip}\n")

    def load_articles(self):
        articles = []
        try:
            with open('articles.txt', 'r') as f:
                for line in f:
                    articles.append(line.strip())
        except FileNotFoundError:
            print("Articles file not found.")
        return articles