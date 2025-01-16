class ArticleManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    headline, summary, source, full_text = line.strip().split(',', 3)
                    articles.append({
                        'headline': headline,
                        'summary': summary,
                        'source': source,
                        'full_text': full_text
                    })
        except FileNotFoundError:
            pass
        return articles

    def get_article_details(self, headline: str) -> dict:
        for article in self.articles:
            if article['headline'] == headline:
                return article
        return {}