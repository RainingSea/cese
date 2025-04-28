class Ranking:
    def rank(self, articles: list, preferences: list) -> list:
        # Simple ranking logic based on preferences
        ranked_articles = sorted(articles, key=lambda x: self.calculate_relevance(x, preferences), reverse=True)
        return ranked_articles

    def calculate_relevance(self, article: str, preferences: list) -> int:
        # Dummy relevance calculation based on preferences
        return sum(1 for pref in preferences if pref in article)