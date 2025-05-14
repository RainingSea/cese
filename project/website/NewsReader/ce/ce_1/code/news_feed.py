import json

class NewsFeed:
    def __init__(self, articles_file='articles.txt'):
        self.articles_file = articles_file

    def _load_articles(self):
        articles = []
        try:
            with open(self.articles_file, 'r') as f:
                for line in f:
                    if line.strip():
                        articles.append(json.loads(line))
        except (IOError, json.JSONDecodeError):
            pass
        return articles

    def get_categories(self):
        articles = self._load_articles()
        categories = set()
        for article in articles:
            categories.add(article['category'])
        return list(categories)

    def search_articles(self, query):
        articles = self._load_articles()
        query = query.lower()
        results = []
        for article in articles:
            if (query in article['title'].lower() or 
                query in article['summary'].lower() or 
                query in article['content'].lower()):
                results.append(article)
        return results

    def get_article_details(self, article_id):
        articles = self._load_articles()
        for article in articles:
            if article['id'] == article_id:
                return article
        return None