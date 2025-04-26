class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
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

    def get_articles_by_category(self, category: str):
        # This function is not implemented in the provided design
        return [article for article in self.articles if article['source'] == category]

    def get_article_details(self, headline: str):
        for article in self.articles:
            if article['headline'] == headline:
                return article
        return None