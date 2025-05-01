import tkinter as tk
from tkinter import messagebox
import json

class Article:
    def __init__(self, title: str, author: str, content: str, category: str):
        self.title = title
        self.author = author
        self.content = content
        self.category = category

    def get_summary(self) -> str:
        return self.content[:100] + '...'  # Return the first 100 characters as summary

class SearchEngine:
    def __init__(self, articles: list):
        self.articles = articles

    def search(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article.title.lower()]

class Favorites:
    def __init__(self):
        self.favorite_articles = []

    def add_favorite(self, article: Article) -> None:
        if article not in self.favorite_articles:
            self.favorite_articles.append(article)

    def remove_favorite(self, article: Article) -> None:
        if article in self.favorite_articles:
            self.favorite_articles.remove(article)

class Annotations:
    def __init__(self):
        self.article_annotations = {}

    def add_annotation(self, article: Article, note: str) -> None:
        if article not in self.article_annotations:
            self.article_annotations[article] = []
        self.article_annotations[article].append(note)

    def get_annotations(self, article: Article) -> list:
        return self.article_annotations.get(article, [])

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Article Manager")
        self.search_engine = None
        self.favorites = Favorites()
        self.annotations = Annotations()
        self.articles = self.load_articles()
        self.search_engine = SearchEngine(self.articles)
        self.create_widgets()

    def load_articles(self) -> list:
        with open('articles.json', 'r') as file:
            articles_data = json.load(file)
            return [Article(**data) for data in articles_data]

    def create_widgets(self):
        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_display = tk.Listbox(self.root)
        self.results_display.pack()

    def perform_search(self):
        query = self.search_bar.get()
        results = self.search_engine.search(query)
        self.results_display.delete(0, tk.END)
        for article in results:
            self.results_display.insert(tk.END, article.title)

    def main(self) -> str:
        self.root.mainloop()
        return "Application closed."

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()