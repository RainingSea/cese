from transformers import pipeline

class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()
        self.bookmarks = self.load_bookmarks()
        self.summarizer = pipeline("summarization")

    def load_articles(self) -> list:
        try:
            with open('articles.txt', 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def save_articles(self) -> None:
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article}\n")

    def summarize_article(self, article: str) -> str:
        summary = self.summarizer(article, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

    def add_bookmark(self, article_id: str) -> None:
        if article_id not in self.bookmarks:
            self.bookmarks.append(article_id)
            self.save_bookmarks()

    def load_bookmarks(self) -> list:
        try:
            with open('bookmarks.txt', 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def save_bookmarks(self) -> None:
        with open('bookmarks.txt', 'w') as file:
            for bookmark in self.bookmarks:
                file.write(f"{bookmark}\n")