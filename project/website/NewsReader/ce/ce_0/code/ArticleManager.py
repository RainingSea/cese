import os

class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

    def save(self) -> None:
        with open('articles.txt', 'a') as file:
            file.write(f"{self.headline},{self.summary},{self.source},{self.full_text}\n")


class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        if not os.path.exists(self.articles_file):
            return articles
        with open(self.articles_file, 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split(',')
                articles.append(Article(headline, summary, source, full_text))
        return articles

    def search_articles(self, keyword: str) -> list:
        results = [article for article in self.articles if keyword.lower() in article.headline.lower()]
        return results if results else ["No articles found"]

    def get_articles_by_category(self, category: str) -> list:
        return [article for article in self.articles if article.source == category]