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
        posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                posts.append(line.strip())
        return posts

    def submit_tip(self, tip: str) -> bool:
        with open('tips.txt', 'a') as file:
            file.write(f"{tip}\n")
        self.tips.append(tip)
        return True

    def submit_article(self, article: str) -> bool:
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")
        self.articles.append(article)
        return True

    def post_to_forum(self, post: str) -> bool:
        with open('forum.txt', 'a') as file:
            file.write(f"{post}\n")
        self.forum_posts.append(post)
        return True

    def get_recent_articles(self):
        return self.articles[-5:]  # Return last 5 articles

    def get_tips(self):
        return self.tips

    def get_forum_posts(self):
        return self.forum_posts