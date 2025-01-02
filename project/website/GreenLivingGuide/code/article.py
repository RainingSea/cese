class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        with open('articles.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                articles.append(Article(title, content))
        return articles