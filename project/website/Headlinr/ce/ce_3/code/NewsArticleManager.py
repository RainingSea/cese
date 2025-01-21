from transformers import pipeline

class NewsArticleManager:
    def __init__(self):
        self.articles = self.load_articles()
        self.summarizer = pipeline("summarization")

    def load_articles(self) -> list:
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    articles.append(line.strip())
        except FileNotFoundError:
            pass
        return articles

    def summarize_article(self, article: str) -> str:
        summary = self.summarizer(article, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def filter_articles(self, preferences: dict) -> list:
        # Placeholder for filtering logic based on user preferences
        return self.articles