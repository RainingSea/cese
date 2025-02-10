class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

    def save(self):
        with open('articles.txt', 'a') as f:
            f.write(f"{self.headline}|{self.summary}|{self.source}|{self.full_text}\n")


class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open(self.articles_file, 'r') as f:
                for line in f:
                    headline, summary, source, full_text = line.strip().split('|')
                    articles.append(Article(headline, summary, source, full_text))
        except FileNotFoundError:
            pass
        return articles

    def add_article(self, article: Article):
        article.save()
        self.articles.append(article)