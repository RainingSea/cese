import tkinter as tk
from tkinter import messagebox
import json
from search_engine import SearchEngine
from favorites_manager import FavoritesManager
from annotation_manager import AnnotationManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Library")
        
        self.search_engine = SearchEngine()
        self.favorites_manager = FavoritesManager()
        self.annotation_manager = AnnotationManager()
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.search_label = tk.Label(self.root, text="Search Articles:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_area = tk.Text(self.root, height=10, width=50)
        self.results_area.pack()

        self.favorite_button = tk.Button(self.root, text="Save as Favorite", command=self.save_favorite)
        self.favorite_button.pack()

        self.annotation_label = tk.Label(self.root, text="Add Annotation:")
        self.annotation_label.pack()

        self.annotation_entry = tk.Entry(self.root)
        self.annotation_entry.pack()

        self.annotate_button = tk.Button(self.root, text="Annotate", command=self.create_annotation)
        self.annotate_button.pack()

    def perform_search(self):
        query = self.search_entry.get()
        results = self.search_engine.search(query)
        self.results_area.delete(1.0, tk.END)
        for article in results:
            self.results_area.insert(tk.END, article + "\n")

    def save_favorite(self):
        selected_article = self.results_area.get("1.0", tk.END).strip().split("\n")
        for article in selected_article:
            if article:
                self.favorites_manager.save_favorite(article)
                messagebox.showinfo("Success", f"'{article}' saved as favorite.")

    def create_annotation(self):
        selected_article = self.results_area.get("1.0", tk.END).strip().split("\n")
        note = self.annotation_entry.get()
        for article in selected_article:
            if article and note:
                self.annotation_manager.create_annotation(article, note)
                messagebox.showinfo("Success", f"Annotation added to '{article}'.")

    def load_data(self):
        self.favorites_manager.load_favorites()
        self.annotation_manager.load_annotations()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()