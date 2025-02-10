class NewsFeed:
    def __init__(self, articles: list):
        self.articles = articles

    def get_articles(self, category: str) -> list:
        return self.articles  # Simplified for demo purposes

    def search_articles(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article.headline.lower()]