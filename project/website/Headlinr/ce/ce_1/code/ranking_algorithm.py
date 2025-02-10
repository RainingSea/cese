class RankingAlgorithm:
    def rank_articles(self, articles: list, preferences: dict) -> list:
        """
        Ranks articles based on user preferences.

        Args:
            articles (list): List of articles to rank.
            preferences (dict): User preferences for ranking.

        Returns:
            list: Ranked list of articles.
        """
        # Simple ranking based on preferences
        ranked_articles = sorted(
            articles, 
            key=lambda article: self.calculate_score(article, preferences), 
            reverse=True
        )
        return ranked_articles

    def calculate_score(self, article: dict, preferences: dict) -> int:
        """
        Calculates a score for an article based on user preferences.

        Args:
            article (dict): The article to score.
            preferences (dict): User preferences.

        Returns:
            int: Score of the article.
        """
        score = 0
        for key, value in preferences.items():
            if key in article and article[key] == value:
                score += 1
        return score