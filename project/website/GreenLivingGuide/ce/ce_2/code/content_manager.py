class ContentManager:
    def __init__(self):
        self.tips = self.load_tips()
        self.articles = self.load_articles()
        self.forum_posts = self.load_forum_posts()

    def load_tips(self):
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                tips.append(line.strip())
        return tips

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles

    def load_forum_posts(self):
        forum_posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                forum_posts.append(line.strip())
        return forum_posts

    def submit_tip(self, tip: str) -> None:
        self.tips.append(tip)
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")

    def submit_article(self, article: str) -> None:
        self.articles.append(article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")

    def submit_forum_post(self, post: str) -> None:
        self.forum_posts.append(post)
        with open('forum.txt', 'a') as file:
            file.write(f"{post}\n")