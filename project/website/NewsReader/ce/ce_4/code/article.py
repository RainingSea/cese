class Article:
    def __init__(self, headline: str = '', summary: str = '', full_text: str = ''):
        self.headline = headline
        self.summary = summary
        self.full_text = full_text

    def save(self):
        with open('articles.txt', 'a') as file:
            file.write(f"{self.headline}|{self.summary}|{self.full_text}\n")

    def load_all(self):
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                article_data = line.strip().split('|')
                if len(article_data) == 3:
                    articles.append(Article(article_data[0], article_data[1], article_data[2]))
        return articles