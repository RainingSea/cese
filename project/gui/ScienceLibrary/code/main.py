import tkinter as tk
from tkinter import messagebox
from article_manager import ArticleManager
from favorites_manager import FavoritesManager
from annotations_manager import AnnotationsManager
from article_viewer import ArticleViewer

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Science Library")
        
        self.article_manager = ArticleManager()
        self.favorites_manager = FavoritesManager()
        self.annotations_manager = AnnotationsManager()
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.search_articles)
        self.search_button.pack()

        self.results_area = tk.Text(self.root, height=10, width=50)
        self.results_area.pack()

        self.view_button = tk.Button(self.root, text="View Article", command=self.view_article)
        self.view_button.pack()

        self.favorite_button = tk.Button(self.root, text="Add to Favorites", command=self.add_to_favorites)
        self.favorite_button.pack()

        self.annotations_area = tk.Text(self.root, height=5, width=50)
        self.annotations_area.pack()

        self.add_annotation_button = tk.Button(self.root, text="Add Annotation", command=self.add_annotation)
        self.add_annotation_button.pack()

        self.organize_favorites_button = tk.Button(self.root, text="Organize Favorites", command=self.organize_favorites)
        self.organize_favorites_button.pack()

    def load_data(self):
        self.article_manager.load_articles()
        self.favorites_manager.load_favorites()
        self.annotations_manager.load_annotations()

    def search_articles(self):
        query = self.search_bar.get()
        results = self.article_manager.search(query)
        self.results_area.delete(1.0, tk.END)
        for article in results:
            self.results_area.insert(tk.END, f"{article}\n")

    def view_article(self):
        selected_article_title = self.results_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        article = self.article_manager.get_article(selected_article_title)
        if article:
            ArticleViewer(article).show()

    def add_to_favorites(self):
        selected_article = self.results_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        self.favorites_manager.add_favorite(selected_article)
        messagebox.showinfo("Info", "Article added to favorites.")

    def add_annotation(self):
        selected_article = self.results_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        note = self.annotations_area.get(1.0, tk.END).strip()
        self.annotations_manager.add_annotation(selected_article, note)
        messagebox.showinfo("Info", "Annotation added.")

    def organize_favorites(self):
        self.favorites_manager.organize_favorites()
        messagebox.showinfo("Info", "Favorites organized.")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()