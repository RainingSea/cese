import http.server
import socketserver
import urllib.parse
import os

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.article_manager = ArticleManager()
        self.forum_manager = ForumManager()

    def main(self):
        PORT = 8000
        handler = self.create_handler()
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"Serving at port {PORT}")
            httpd.serve_forever()

    def create_handler(self):
        return http.server.SimpleHTTPRequestHandler

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        if not os.path.exists('tips.txt'):
            return []
        with open('tips.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def submit_tip(self, tip: str) -> None:
        self.tips.append(tip)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")

    def get_tips(self) -> list:
        return self.tips

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        if not os.path.exists('articles.txt'):
            return []
        with open('articles.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def submit_article(self, article: str) -> None:
        self.articles.append(article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")

    def get_articles(self) -> list:
        return self.articles

class ForumManager:
    def __init__(self):
        self.posts = self.load_posts()

    def load_posts(self):
        if not os.path.exists('forum.txt'):
            return []
        with open('forum.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def submit_post(self, post: str) -> None:
        self.posts.append(post)
        with open('forum.txt', 'a') as file:
            file.write(f"{post}\n")

    def get_posts(self) -> list:
        return self.posts

if __name__ == "__main__":
    app = Main()
    app.main()