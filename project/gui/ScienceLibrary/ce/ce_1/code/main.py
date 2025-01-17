import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Text
from search_engine import SearchEngine

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Article Organizer")
        self.search_engine = SearchEngine()

        self.search_bar = tk.Entry(root)
        self.search_bar.pack()

        self.search_button = tk.Button(root, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.result_listbox = Listbox(root)
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.bind('<<ListboxSelect>>', self.show_article_details)

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result_listbox.yview)

        self.details_text = Text(root, height=10)
        self.details_text.pack()

    def perform_search(self):
        query = self.search_bar.get()
        results = self.search_engine.search(query)
        self.result_listbox.delete(0, tk.END)
        for article in results:
            self.result_listbox.insert(tk.END, article['title'])

    def show_article_details(self, event):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            article_title = self.result_listbox.get(selected_index)
            article = next((a for a in self.search_engine.article_repo.data if a['title'] == article_title), {})
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Title: {article.get('title', 'N/A')}\n")
            self.details_text.insert(tk.END, f"Author: {article.get('author', 'N/A')}\n")
            self.details_text.insert(tk.END, f"Abstract: {article.get('abstract', 'N/A')}\n")

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()