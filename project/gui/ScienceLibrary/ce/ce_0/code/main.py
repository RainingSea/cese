import tkinter as tk
from SearchEngine import SearchEngine
from ArticleManager import ArticleManager

class Main:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.article_manager = ArticleManager()
        self.article_manager.load_articles('articles.json')
        self.setup_ui()

    def setup_ui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Science Library")

        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_area = tk.Text(self.root)
        self.results_area.pack()

        self.root.mainloop()

    def perform_search(self) -> None:
        query = self.search_bar.get()
        results = self.search_engine.search(query)
        self.results_area.delete(1.0, tk.END)
        for article in results:
            self.results_area.insert(tk.END, f"{article['title']}\n{article['content']}\n\n")

if __name__ == "__main__":
    Main()