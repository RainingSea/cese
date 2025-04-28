from user_profile import UserProfile
from article_processor import ArticleProcessor
from ranking import Ranking

class SearchEngine:
    def __init__(self):
        self.user_profile = UserProfile()
        self.article_processor = ArticleProcessor()
        self.ranking = Ranking()

    def generate_summary(self, article: str) -> str:
        return self.article_processor.extract_key_information(article)

    def rank_articles(self, user_preferences: list) -> list:
        articles = self.load_articles()
        return self.ranking.rank(articles, user_preferences)

    def load_articles(self) -> list:
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles