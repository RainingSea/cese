import tkinter as tk
from tkinter import messagebox
import json

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.snippet_manager.load_snippets()
        self.root = tk.Tk()
        self.root.title("Snippet Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=True, fill='both')

        self.save_button = tk.Button(self.root, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack(side='left')

        self.search_button = tk.Button(self.root, text="Search Snippet", command=self.search_snippet)
        self.search_button.pack(side='right')

    def save_snippet(self):
        snippet = self.text_area.get("1.0", tk.END).strip()
        if snippet:
            tags = self.get_tags()
            description = self.get_description()
            self.snippet_manager.add_snippet(snippet, tags, description)
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Snippet saved successfully!")
        else:
            messagebox.showwarning("Warning", "Snippet cannot be empty!")

    def search_snippet(self):
        query = self.text_area.get("1.0", tk.END).strip()
        results = self.snippet_manager.search_snippet(query)
        if results:
            messagebox.showinfo("Search Results", "\n".join(results))
        else:
            messagebox.showinfo("Search Results", "No snippets found.")

    def get_tags(self):
        # Placeholder for tag retrieval logic
        return []

    def get_description(self):
        # Placeholder for description retrieval logic
        return ""

def main():
    app = Main()

if __name__ == "__main__":
    main()