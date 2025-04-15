class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

    def save(self):
        with open('articles.txt', 'a') as file:
            file.write(f"{self.headline},{self.summary},{self.source},{self.full_text}\n")


class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def load_articles(self):
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    headline, summary, source, full_text = line.strip().split(',')
                    self.articles.append(Article(headline, summary, source, full_text))
        except FileNotFoundError:
            pass

    def search_articles(self, query: str):
        results = [article for article in self.articles if query.lower() in article.headline.lower()]
        if not results:
            return "No articles found"
        return results

    def get_article(self, index: int) -> Article:
        return self.articles[index] if 0 <= index < len(self.articles) else None