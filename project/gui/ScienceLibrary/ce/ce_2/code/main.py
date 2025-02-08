import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from search_engine import SearchEngine

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Science Library")
        self.search_engine = SearchEngine()

        self.search_label = tk.Label(master, text="Search Articles:")
        self.search_label.pack()

        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.perform_search)
        self.search_button.pack()

        self.results_listbox = Listbox(master)
        self.results_listbox.pack()

        self.save_button = tk.Button(master, text="Save Favorite", command=self.save_favorite)
        self.save_button.pack()

        self.annotation_button = tk.Button(master, text="Add Annotation", command=self.add_annotation)
        self.annotation_button.pack()

    def perform_search(self):
        query = self.search_entry.get()
        results = self.search_engine.search(query)
        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result)

    def save_favorite(self):
        selected_article = self.results_listbox.curselection()
        if selected_article:
            article_id = self.results_listbox.get(selected_article)
            self.search_engine.article_manager.save_favorite(article_id)
            messagebox.showinfo("Success", f"Saved '{article_id}' to favorites.")

    def add_annotation(self):
        selected_article = self.results_listbox.curselection()
        if selected_article:
            article_id = self.results_listbox.get(selected_article)
            annotation = simpledialog.askstring("Input", "Enter your annotation:")
            if annotation:
                self.search_engine.article_manager.add_annotation(article_id, annotation)
                messagebox.showinfo("Success", f"Annotation added to '{article_id}'.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()