from user import User
from article import Article

class SocialShare:
    def __init__(self, users_file: str, articles_file: str):
        self.users_file = users_file
        self.articles_file = articles_file
        self.users = self.load_users()
        self.articles = self.load_articles()

    def load_users(self):
        users = []
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password, bio = line.strip().split('|')
                    users.append(User(username, password, bio))
        except FileNotFoundError:
            pass
        return users

    def load_articles(self):
        articles = []
        try:
            with open(self.articles_file, 'r') as f:
                for line in f:
                    title, content, author = line.strip().split('|')
                    articles.append(Article(title, content, author))
        except FileNotFoundError:
            pass
        return articles

    def register_user(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        return True

    def login_user(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def add_article(self, title: str, content: str, author: str):
        new_article = Article(title, content, author)
        self.articles.append(new_article)
        self.save_articles()

    def get_feed(self) -> list:
        return self.articles

    def update_user_bio(self, username: str, new_bio: str):
        for user in self.users:
            if user.username == username:
                user.update_bio(new_bio)
                self.save_users()
                break

    def save_users(self):
        with open(self.users_file, 'w') as f:
            for user in self.users:
                f.write(f"{user.username}|{user.password}|{user.bio}\n")

    def save_articles(self):
        with open(self.articles_file, 'w') as f:
            for article in self.articles:
                f.write(f"{article.title}|{article.content}|{article.author}\n")