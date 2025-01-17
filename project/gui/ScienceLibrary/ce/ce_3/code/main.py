import tkinter as tk
from search_engine import SearchEngine
from article_manager import ArticleManager
from article import Article

class Main:
    def __init__(self):
        self.search_engine = SearchEngine('articles.json')
        self.article_manager = ArticleManager('saved_articles.json', 'annotations.json')
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Article Manager")
        
        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_listbox = tk.Listbox(self.root)
        self.results_listbox.pack()

        self.save_button = tk.Button(self.root, text="Save Article", command=self.save_article)
        self.save_button.pack()

        self.root.mainloop()

    def perform_search(self):
        query = self.search_bar.get()
        results = self.search_engine.search(query)
        self.results_listbox.delete(0, tk.END)
        for article in results:
            self.results_listbox.insert(tk.END, article.title)

    def save_article(self):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            selected_article = self.search_engine.articles[selected_index[0]]
            self.article_manager.save_article(selected_article)

if __name__ == "__main__":
    Main()