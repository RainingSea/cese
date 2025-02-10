class RankingSystem:
    def rank_articles(self, articles: list, preferences: dict) -> list:
        ranked_articles = sorted(articles, key=lambda x: sum(1 for topic in preferences.get('topics', []) if topic in x.title), reverse=True)
        return ranked_articles