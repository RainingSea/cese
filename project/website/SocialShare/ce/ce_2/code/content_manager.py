class ContentManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles

    def shareArticle(self, username: str, article: str) -> None:
        self.articles.append(f"{username}|{article}")
        self.save_articles()

    def save_articles(self):
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article}\n")

    def getFeed(self) -> list:
        return self.articles

    def likeArticle(self, username: str, article_id: int) -> None:
        # Placeholder for liking an article
        pass

    def commentOnArticle(self, username: str, article_id: int, comment: str) -> None:
        # Placeholder for commenting on an article
        pass