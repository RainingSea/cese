class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

class ArticleManager:
    def __init__(self):
        self.articles = []
        self.load_articles()

    def load_articles(self) -> None:
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.articles.append(Article(title, content))
        except FileNotFoundError:
            pass

    def save_articles(self) -> None:
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article.title}|{article.content}\n")

    def get_articles_by_preferences(self, preferences: dict) -> list:
        filtered_articles = []
        for article in self.articles:
            if any(topic in article.title for topic in preferences.get('topics', [])):
                filtered_articles.append(article)
        return filtered_articles