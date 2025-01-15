class ArticleManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    articles.append(line.strip())
        except FileNotFoundError:
            pass
        return articles

    def search_articles(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article.lower()]