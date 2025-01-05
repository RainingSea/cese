from models import User, Tip, Article, ForumPost

class DataManager:
    def load_users(self) -> List[User]:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
                users.append(User(username=username, password=password))
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def load_tips(self) -> List[Tip]:
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                content, author = line.strip().split('|')
                tips.append(Tip(content=content, author=author))
        return tips

    def save_tip(self, tip: Tip):
        with open('tips.txt', 'a') as file:
            file.write(f"{tip.content}|{tip.author}\n")

    def load_articles(self) -> List[Article]:
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                articles.append(Article(title=title, content=content, author=author))
        return articles

    def save_article(self, article: Article):
        with open('articles.txt', 'a') as file:
            file.write(f"{article.title}|{article.content}|{article.author}\n")

    def load_forum_posts(self) -> List[ForumPost]:
        posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                content, author = line.strip().split('|')
                posts.append(ForumPost(content=content, author=author))
        return posts

    def save_forum_post(self, post: ForumPost):
        with open('forum.txt', 'a') as file:
            file.write(f"{post.content}|{post.author}\n")