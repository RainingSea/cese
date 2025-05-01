import tkinter as tk
import json

class Main:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.article_manager = ArticleManager()

    def main(self):
        self.root = tk.Tk()
        self.root.title("Article Search App")

        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_display = tk.Text(self.root)
        self.results_display.pack()

        self.root.mainloop()

    def perform_search(self):
        query = self.search_bar.get()
        results = self.search_engine.search(query)
        self.display_results(results)

    def display_results(self, results):
        self.results_display.delete(1.0, tk.END)
        for article in results:
            self.results_display.insert(tk.END, f"{article}\n")

class SearchEngine:
    def __init__(self):
        self.articles = self.load_articles()

    def load_articles(self):
        with open('articles.json', 'r') as file:
            return json.load(file)

    def search(self, query: str) -> list:
        return [article for article in self.articles if query.lower() in article['title'].lower()]

    def sort(self, criteria: str) -> list:
        return sorted(self.articles, key=lambda x: x[criteria])

class ArticleManager:
    def __init__(self):
        self.favorites = self.load_favorites()
        self.annotations = self.load_annotations()

    def load_favorites(self):
        with open('favorites.json', 'r') as file:
            return json.load(file)

    def load_annotations(self):
        with open('annotations.json', 'r') as file:
            return json.load(file)

    def save_favorite(self, article_id: str) -> None:
        self.favorites.append(article_id)
        self.save_to_file('favorites.json', self.favorites)

    def organize_favorites(self) -> None:
        # Placeholder for organizing favorites logic
        pass

    def add_annotation(self, article_id: str, note: str) -> None:
        self.annotations[article_id] = note
        self.save_to_file('annotations.json', self.annotations)

    def save_to_file(self, filename: str, data) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file)

if __name__ == "__main__":
    app = Main()
    app.main()