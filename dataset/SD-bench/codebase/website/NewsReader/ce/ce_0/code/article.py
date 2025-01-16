class Article:
    def __init__(self, headline: str, summary: str, source: str, full_text: str):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text

    def save(self):
        with open('articles.txt', 'a') as file:
            file.write(f"{self.headline}|{self.summary}|{self.source}|{self.full_text}\n")

    @staticmethod
    def load_all():
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split('|')
                articles.append(Article(headline, summary, source, full_text))
        return articles