class User:
    def __init__(self, username: str, password: str, bio: str):
        self.username = username
        self.password = password
        self.bio = bio

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.bio}"

class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def to_string(self) -> str:
        return f"{self.title}|{self.content}|{self.author}"

class Comment:
    def __init__(self, article_id: int, user: str, comment: str):
        self.article_id = article_id
        self.user = user
        self.comment = comment

    def to_string(self) -> str:
        return f"{self.article_id}|{self.user}|{self.comment}"

class SocialShare:
    def __init__(self, users_file: str, articles_file: str, comments_file: str):
        self.users_file = users_file
        self.articles_file = articles_file
        self.comments_file = comments_file

    def register_user(self, username: str, password: str, bio: str) -> bool:
        user = User(username, password, bio)
        with open(self.users_file, 'a') as f:
            f.write(user.to_string() + '\n')
        return True

    def login_user(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password, _ = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def create_article(self, title: str, content: str, author: str) -> bool:
        article = Article(title, content, author)
        with open(self.articles_file, 'a') as f:
            f.write(article.to_string() + '\n')
        return True

    def add_comment(self, article_id: int, user: str, comment: str) -> bool:
        comment_obj = Comment(article_id, user, comment)
        with open(self.comments_file, 'a') as f:
            f.write(comment_obj.to_string() + '\n')
        return True

    def get_feed(self) -> list:
        articles = []
        with open(self.articles_file, 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                articles.append(Article(title, content, author))
        return articles

    def get_user_profile(self, username: str) -> User:
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password, bio = line.strip().split('|')
                if stored_username == username:
                    return User(stored_username, stored_password, bio)
        return None