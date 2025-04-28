import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.content_manager = ContentManager()

    def main(self):
        self.user_manager.load_users()
        self.content_manager.load_articles()
        self.user_manager.load_profiles()
        self.content_manager.load_interactions()

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})

    def register(self, username: str, password: str) -> bool:
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def load_profiles(self):
        if os.path.exists('profiles.txt'):
            with open('profiles.txt', 'r') as file:
                for line in file:
                    username, bio = line.strip().split('|')
                    # Assuming we store profiles in a dictionary for simplicity
                    for user in self.users:
                        if user['username'] == username:
                            user['bio'] = bio

    def update_profile(self, username: str, bio: str) -> bool:
        for user in self.users:
            if user['username'] == username:
                user['bio'] = bio
                with open('profiles.txt', 'a') as file:
                    file.write(f"{username}|{bio}\n")
                return True
        return False

class ContentManager:
    def __init__(self):
        self.articles = []
        self.interactions = []

    def load_articles(self):
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    self.articles.append({'title': title, 'content': content, 'author': author})

    def share_article(self, title: str, content: str, author: str) -> bool:
        self.articles.append({'title': title, 'content': content, 'author': author})
        with open('articles.txt', 'a') as file:
            file.write(f"{title}|{content}|{author}\n")
        return True

    def get_feed(self) -> list:
        return self.articles

    def load_interactions(self):
        if os.path.exists('interactions.txt'):
            with open('interactions.txt', 'r') as file:
                for line in file:
                    action, article_id, user_id = line.strip().split('|')
                    self.interactions.append({'action': action, 'article_id': int(article_id), 'user_id': int(user_id)})

    def like_article(self, article_id: int, user_id: int) -> bool:
        self.interactions.append({'action': 'like', 'article_id': article_id, 'user_id': user_id})
        with open('interactions.txt', 'a') as file:
            file.write(f"like|{article_id}|{user_id}\n")
        return True

    def comment_on_article(self, article_id: int, user_id: int, comment: str) -> bool:
        self.interactions.append({'action': 'comment', 'article_id': article_id, 'user_id': user_id, 'comment': comment})
        with open('interactions.txt', 'a') as file:
            file.write(f"comment|{article_id}|{user_id}|{comment}\n")
        return True

if __name__ == "__main__":
    app = Main()
    app.main()