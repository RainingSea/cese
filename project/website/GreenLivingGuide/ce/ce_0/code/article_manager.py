class ArticleManager:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                articles.append(line.strip())
        return articles

    def submit_article(self, article: str) -> bool:
        self.articles.append(article)
        with open('articles.txt', 'a') as file:
            file.write(f"{article}\n")
        return True

    def get_recent_articles(self):
        return self.articles[-5:]  # Return the last 5 articles