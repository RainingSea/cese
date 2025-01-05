class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")


class Tip:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('tips.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")


class Article:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.author}\n")


class ForumPost:
    def __init__(self, content: str, author: str):
        self.content = content
        self.author = author

    def save(self):
        with open('forum.txt', 'a') as f:
            f.write(f"{self.content}|{self.author}\n")


class DataManager:
    def load_users(self):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def save_user(self, user: User):
        user.save()

    def load_tips(self):
        tips = []
        with open('tips.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                tips.append(Tip(content, author))
        return tips

    def save_tip(self, tip: Tip):
        tip.save()

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as f:
            for line in f:
                title, content, author = line.strip().split('|')
                articles.append(Article(title, content, author))
        return articles

    def save_article(self, article: Article):
        article.save()

    def load_forum_posts(self):
        posts = []
        with open('forum.txt', 'r') as f:
            for line in f:
                content, author = line.strip().split('|')
                posts.append(ForumPost(content, author))
        return posts

    def save_forum_post(self, post: ForumPost):
        post.save()