from User import User
from Tip import Tip
from Article import Article
from ForumPost import ForumPost

class DataManager:
    def load_users(self) -> list[User]:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(user.to_string() + '\n')

    def load_tips(self) -> list[Tip]:
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                tips.append(Tip(line.strip()))
        return tips

    def save_tip(self, tip: Tip):
        with open('tips.txt', 'a') as file:
            file.write(tip.to_string() + '\n')

    def load_articles(self) -> list[Article]:
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                articles.append(Article(title, content))
        return articles

    def save_article(self, article: Article):
        with open('articles.txt', 'a') as file:
            file.write(article.to_string() + '\n')

    def load_forum_posts(self) -> list[ForumPost]:
        posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                username, content = line.strip().split('|')
                posts.append(ForumPost(username, content))
        return posts

    def save_forum_post(self, post: ForumPost):
        with open('forum.txt', 'a') as file:
            file.write(post.to_string() + '\n')