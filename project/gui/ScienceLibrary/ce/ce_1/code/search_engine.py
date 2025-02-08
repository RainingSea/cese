from article_repository import ArticleRepository

class SearchEngine:
    def __init__(self):
        self.article_repo = ArticleRepository()

    def search(self, query: str) -> List[Dict]:
        return [article for article in self.article_repo.data if query.lower() in article['title'].lower()]

    def get_article_details(self, article_id: str) -> Dict:
        for article in self.article_repo.data:
            if article['id'] == article_id:
                return article
        return {}