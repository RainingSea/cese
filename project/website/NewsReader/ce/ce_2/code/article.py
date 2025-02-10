from file_manager import FileManager

class Article:
    def __init__(self, headline: str = '', summary: str = '', source: str = '', full_text: str = ''):
        self.headline = headline
        self.summary = summary
        self.source = source
        self.full_text = full_text
        self.file_manager = FileManager()

    def save_article(self) -> bool:
        return self.file_manager.write_article(self)

    def get_articles(self) -> list:
        return self.file_manager.read_articles()