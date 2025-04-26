import nltk

class NLTKProcessor:
    def summarize(self, article: str) -> str:
        # Summarization logic using NLTK
        return article[:100]  # Simple example: return first 100 characters

    def rank_articles(self, articles: list, preferences: str) -> list:
        # Ranking logic based on preferences
        return sorted(articles)  # Simple example: sort articles alphabetically