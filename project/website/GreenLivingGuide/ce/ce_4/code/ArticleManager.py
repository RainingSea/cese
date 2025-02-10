class ArticleManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open(self.filename, 'r') as file:
                articles = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return articles

    def submit_article(self, article: str) -> None:
        with open(self.filename, 'a') as file:
            file.write(f"{article}\n")
        self.articles.append(article)