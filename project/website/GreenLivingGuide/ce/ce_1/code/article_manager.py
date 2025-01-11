class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                articles = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return articles

    def save_articles(self) -> bool:
        try:
            with open('articles.txt', 'w') as file:
                for article in self.articles:
                    file.write(f"{article}\n")
            return True
        except Exception as e:
            print(f"Error saving articles: {e}")
            return False

    def add_article(self, article: str) -> bool:
        self.articles.append(article)
        return self.save_articles()