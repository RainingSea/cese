import tkinter as tk
from snippet_manager import SnippetManager

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.snippet_manager.load_snippets()
        self.root = tk.Tk()
        self.root.title("Snippet Manager")
        self.create_widgets()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=True, fill='both')

        self.save_button = tk.Button(self.root, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack(side='bottom')

    def save_snippet(self):
        text = self.text_area.get("1.0", tk.END).strip()
        tags = []  # Tags can be added through another input method
        description = "Snippet description"  # Description can be added through another input method
        self.snippet_manager.add_snippet(text, tags, description)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()