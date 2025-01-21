class RankingAlgorithm:
    def rank_articles(self, articles: list, preferences: dict) -> list:
        # Simple ranking based on preferences
        ranked_articles = sorted(articles, key=lambda x: self._calculate_score(x, preferences), reverse=True)
        return ranked_articles

    def _calculate_score(self, article: dict, preferences: dict) -> int:
        score = 0
        for key, value in preferences.items():
            if key in article and article[key] == value:
                score += 1
        return score