class ContentManager:
    def __init__(self):
        self.articles = self.load_articles()
        self.interactions = self.load_interactions()

    def load_articles(self):
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    articles.append(line.strip())
        except FileNotFoundError:
            pass
        return articles

    def load_interactions(self):
        interactions = {}
        try:
            with open('interactions.txt', 'r') as file:
                for line in file:
                    username, article_id, action = line.strip().split('|')
                    if article_id not in interactions:
                        interactions[article_id] = []
                    interactions[article_id].append((username, action))
        except FileNotFoundError:
            pass
        return interactions

    def share_article(self, username: str, article: str) -> bool:
        self.articles.append(article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")
        return True

    def like_article(self, username: str, article_id: int) -> bool:
        if article_id < len(self.articles):
            self.interactions.setdefault(article_id, []).append((username, 'like'))
            with open('interactions.txt', 'a') as file:
                file.write(f"{username}|{article_id}|like\n")
            return True
        return False

    def comment_on_article(self, username: str, article_id: int, comment: str) -> bool:
        if article_id < len(self.articles):
            self.interactions.setdefault(article_id, []).append((username, 'comment', comment))
            with open('interactions.txt', 'a') as file:
                file.write(f"{username}|{article_id}|comment|{comment}\n")
            return True
        return False

    def get_feed(self) -> list:
        return self.articles