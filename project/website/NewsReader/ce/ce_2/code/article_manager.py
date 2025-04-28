class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self) -> list:
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    headline, summary, source, full_text = line.strip().split(',')
                    articles.append({
                        'headline': headline,
                        'summary': summary,
                        'source': source,
                        'full_text': full_text
                    })
        except FileNotFoundError:
            pass
        return articles

    def search_articles(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article['headline'].lower()]