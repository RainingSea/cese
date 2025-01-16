class ArticleManager:
    def __init__(self, article_file: str):
        self.article_file = article_file
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open(self.article_file, 'r') as f:
                for line in f:
                    articles.append(line.strip())
        except FileNotFoundError:
            pass
        return articles

    def get_article_details(self, title: str) -> str:
        for article in self.articles:
            if article.startswith(title):
                return article
        return "Article not found."