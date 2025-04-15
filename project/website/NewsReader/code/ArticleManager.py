from typing import List

class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

class ArticleManager:
    def __init__(self):
        self.articles: List[Article] = []
        self.load_articles()

    def load_articles(self) -> None:
        """Load articles from a file."""
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    headline, summary, source, full_text = line.strip().split('|')
                    self.articles.append(Article(headline, summary, source, full_text))
        except FileNotFoundError:
            pass

    def save_articles(self) -> None:
        """Save articles to a file."""
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article.headline}|{article.summary}|{article.source}|{article.full_text}\n")

    def search_articles(self, keyword: str) -> List[Article]:
        """Search for articles containing the given keyword."""
        return [article for article in self.articles if keyword.lower() in article.headline.lower() or keyword.lower() in article.summary.lower()]