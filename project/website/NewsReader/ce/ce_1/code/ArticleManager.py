class Article:
    def __init__(self, title: str, summary: str, source: str, full_text: str):
        self.title = title
        self.summary = summary
        self.source = source
        self.full_text = full_text

class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def load_articles(self) -> None:
        """Load articles from the articles.txt file."""
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, summary, source, full_text = line.strip().split('|')
                    self.articles.append(Article(title, summary, source, full_text))
        except FileNotFoundError:
            pass

    def save_articles(self) -> None:
        """Save articles to the articles.txt file."""
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article.title}|{article.summary}|{article.source}|{article.full_text}\n")

    def search_articles(self, query: str) -> list[Article]:
        """Search for articles containing the query in their title."""
        return [article for article in self.articles if query.lower() in article.title.lower()]

    def get_article_details(self, title: str) -> Article:
        """Get details of an article by its title."""
        for article in self.articles:
            if article.title == title:
                return article
        return None