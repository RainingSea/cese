class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

    def get_details(self) -> str:
        return self.full_text


class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file

    def load_articles(self) -> list:
        articles = []
        with open(self.articles_file, 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split(',')
                articles.append(Article(headline, summary, source, full_text))
        return articles

    def save_article(self, article: Article) -> None:
        with open(self.articles_file, 'a') as file:
            file.write(f"{article.headline},{article.summary},{article.source},{article.full_text}\n")