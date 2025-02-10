class FileManager:
    def read_users(self) -> list:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append((username, password))
        return users

    def write_user(self, user) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")
        return True

    def read_articles(self) -> list:
        articles = []
        with open('articles.txt', 'r') as file:
            for line in file:
                headline, summary, source, full_text = line.strip().split('|')
                articles.append(Article(headline, summary, source, full_text))
        return articles

    def write_article(self, article) -> bool:
        with open('articles.txt', 'a') as file:
            file.write(f"{article.headline}|{article.summary}|{article.source}|{article.full_text}\n")
        return True