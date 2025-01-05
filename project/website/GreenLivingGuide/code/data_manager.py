import os
from user import User
from tip import Tip
from article import Article
from forum_post import ForumPost

class DataManager:
    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, _ = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_user(self, user):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}|\n")

    def load_tips(self):
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                for line in file:
                    content, author = line.strip().split('|')
                    tips.append(Tip(content, author))
        return tips

    def save_tip(self, tip):
        with open('tips.txt', 'a') as file:
            file.write(f"{tip.content}|{tip.author}\n")

    def load_articles(self):
        articles = []
        if os.path.exists('articles.txt'):
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    articles.append(Article(title, content, author))
        return articles

    def save_article(self, article):
        with open('articles.txt', 'a') as file:
            file.write(f"{article.title}|{article.content}|{article.author}\n")

    def load_forum_posts(self):
        posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as file:
                for line in file:
                    content, author = line.strip().split('|')
                    posts.append(ForumPost(content, author))
        return posts

    def save_forum_post(self, post):
        with open('forum.txt', 'a') as file:
            file.write(f"{post.content}|{post.author}\n")