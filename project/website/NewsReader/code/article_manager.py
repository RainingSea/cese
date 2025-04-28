class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        with open(self.articles_file, 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles

    def search_articles(self, keyword: str) -> list:
        return [article for article in self.articles if keyword.lower() in article.lower()]

    def get_article_details(self, article_id: int) -> str:
        if 0 <= article_id < len(self.articles):
            return self.articles[article_id]
        return "Article not found."