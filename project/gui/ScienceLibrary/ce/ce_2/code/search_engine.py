from article_manager import ArticleManager

class SearchEngine:
    def __init__(self):
        self.article_manager = ArticleManager()

    def search(self, query: str):
        results = []
        for article in self.article_manager.articles:
            if query.lower() in article.lower():
                results.append(article)
        return results