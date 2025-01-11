import os

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        """Load articles from the articles.txt file."""
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                articles = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return articles

    def save_articles(self) -> None:
        """Save articles to the articles.txt file."""
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article}\n")

    def add_article(self, article: str) -> bool:
        """Add a new article and save to the file."""
        self.articles.append(article)
        self.save_articles()
        return self.verify_article_data()

    def get_articles(self) -> list:
        """Retrieve all articles."""
        return self.articles

    def verify_article_data(self) -> bool:
        """Verify if article data is correctly saved."""
        current_articles = self.load_articles()
        return current_articles == self.articles