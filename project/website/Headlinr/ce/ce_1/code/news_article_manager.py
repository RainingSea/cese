from transformers import pipeline

class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class NewsArticleManager:
    def __init__(self):
        self.articles = self.load_articles()
        self.summarizer = pipeline("summarization")

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                articles.append(Article(title, content))
        return articles

    def summarize_article(self, article: Article) -> str:
        summary = self.summarizer(article.content, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

    def rank_articles(self, preferences: list) -> list:
        # Simple ranking based on preferences (not implemented)
        return self.articles