class ArticleManager:
    def __init__(self, articles_file: str):
        self.articles_file = articles_file
        self.load_articles()

    def load_articles(self):
        self.articles = {}
        with open(self.articles_file, 'r') as file:
            for line in file:
                article_id, title, content = line.strip().split('|')
                self.articles[article_id] = {'title': title, 'content': content}

    def get_articles(self, category: str) -> list:
        return [{'id': article_id, 'title': article['title']} for article_id, article in self.articles.items()]

    def get_article_details(self, article_id: str) -> dict:
        return self.articles.get(article_id, {})