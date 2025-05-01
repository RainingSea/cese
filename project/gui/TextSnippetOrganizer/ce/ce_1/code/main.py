import tkinter as tk
from tkinter import messagebox
from typing import List

class SnippetManager:
    def __init__(self):
        self.snippets = []
        self.tags = []
        self.descriptions = []
        self.load_snippets()

    def add_snippet(self, snippet: str, tags: List[str], description: str) -> None:
        self.snippets.append(snippet)
        self.tags.append(', '.join(tags))
        self.descriptions.append(description)
        self.save_snippets()

    def load_snippets(self) -> None:
        try:
            with open('snippets.txt', 'r') as f:
                self.snippets = f.read().strip().splitlines()
            with open('tags.txt', 'r') as f:
                self.tags = f.read().strip().splitlines()
            with open('descriptions.txt', 'r') as f:
                self.descriptions = f.read().strip().splitlines()
        except FileNotFoundError:
            self.snippets = []
            self.tags = []
            self.descriptions = []

    def save_snippets(self) -> None:
        with open('snippets.txt', 'w') as f:
            f.write('\n'.join(self.snippets))
        with open('tags.txt', 'w') as f:
            f.write('\n'.join(self.tags))
        with open('descriptions.txt', 'w') as f:
            f.write('\n'.join(self.descriptions))

class UI:
    def __init__(self, main):
        self.main = main
        self.window = tk.Tk()
        self.window.title("Text Snippet Organizer")
        self.create_widgets()

    def create_widgets(self):
        self.snippet_label = tk.Label(self.window, text="Snippet:")
        self.snippet_label.pack()
        self.snippet_input = tk.Entry(self.window, width=50)
        self.snippet_input.pack()

        self.tag_label = tk.Label(self.window, text="Tags (comma separated):")
        self.tag_label.pack()
        self.tag_input = tk.Entry(self.window, width=50)
        self.tag_input.pack()

        self.description_label = tk.Label(self.window, text="Description:")
        self.description_label.pack()
        self.description_input = tk.Entry(self.window, width=50)
        self.description_input.pack()

        self.save_button = tk.Button(self.window, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack()

        self.display_area = tk.Text(self.window, height=10, width=50)
        self.display_area.pack()

        self.load_snippets()

    def save_snippet(self):
        snippet = self.snippet_input.get()
        tags = self.tag_input.get().split(',')
        description = self.description_input.get()

        if snippet:
            self.main.snippet_manager.add_snippet(snippet, tags, description)
            self.display_snippet(snippet)
            self.clear_inputs()
        else:
            messagebox.showwarning("Warning", "Snippet cannot be empty!")

    def load_snippets(self):
        for snippet in self.main.snippet_manager.snippets:
            self.display_snippet(snippet)

    def display_snippet(self, snippet: str) -> None:
        self.display_area.insert(tk.END, snippet + '\n')

    def clear_inputs(self):
        self.snippet_input.delete(0, tk.END)
        self.tag_input.delete(0, tk.END)
        self.description_input.delete(0, tk.END)

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.ui = UI(self)

    def main(self) -> str:
        self.ui.window.mainloop()
        return "Application closed."

if __name__ == "__main__":
    app = Main()
    app.main()