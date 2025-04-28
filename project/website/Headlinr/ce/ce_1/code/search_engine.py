import json
from ranking import Ranking
from summary import Summary

class SearchEngine:
    def __init__(self):
        self.index = {}
        self.ranking = Ranking()
        self.summary = Summary()

    def search(self, query: str) -> list:
        # Simulated search logic
        articles = self.index.get(query, [])
        ranked_articles = self.ranking.rank_articles(articles)
        return [self.summary.generate_summary(article) for article in ranked_articles]