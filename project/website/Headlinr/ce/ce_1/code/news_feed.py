import json

class NewsFeed:
    def __init__(self):
        self.articles = self.load_articles()
        self.ranking_algorithm = RankingAlgorithm()

    def load_articles(self) -> list:
        """
        Loads articles from a text file.

        Returns:
            list: List of articles.
        """
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    article = json.loads(line.strip())
                    articles.append(article)
        except FileNotFoundError:
            pass
        return articles

    def generate_summaries(self, preferences: dict) -> list:
        """
        Generates summaries of articles based on user preferences.

        Args:
            preferences (dict): User preferences for summarization.

        Returns:
            list: List of summarized articles.
        """
        ranked_articles = self.ranking_algorithm.rank_articles(self.articles, preferences)
        summaries = [{"title": article["title"], "summary": article["summary"]} for article in ranked_articles]
        return summaries

    def bookmark_article(self, article_id: str, user_id: str) -> None:
        """
        Bookmarks an article for a user.

        Args:
            article_id (str): The ID of the article to bookmark.
            user_id (str): The ID of the user who bookmarks the article.
        """
        with open('bookmarks.txt', 'a') as file:
            file.write(f"{user_id}|{article_id}\n")