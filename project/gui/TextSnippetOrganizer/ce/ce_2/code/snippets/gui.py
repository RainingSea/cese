import tkinter as tk
from tkinter import scrolledtext, messagebox
from snippets.snippet_manager import SnippetManager

class GUI:
    def __init__(self, root: tk.Tk):
        self.snippet_manager = SnippetManager()
        self.snippet_manager.load_snippets()
        self.create_widgets()

    def create_widgets(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)

        self.tag_entry = tk.Entry(self.root)
        self.tag_entry.pack(padx=10, pady=5)

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack(padx=10, pady=5)

        self.save_button = tk.Button(self.root, text='Save Snippet', command=self.save_snippet)
        self.save_button.pack(pady=5)

        self.retrieve_button = tk.Button(self.root, text='Retrieve Snippets', command=self.retrieve_snippets)
        self.retrieve_button.pack(pady=5)

    def save_snippet(self):
        text = self.text_area.get("1.0", tk.END).strip()
        tags = self.tag_entry.get().split(',')
        description = self.description_entry.get().strip()
        if text and tags:
            self.snippet_manager.add_snippet(text, [tag.strip() for tag in tags], description)
            messagebox.showinfo("Success", "Snippet saved successfully!")
        else:
            messagebox.showwarning("Warning", "Text and tags cannot be empty!")

    def retrieve_snippets(self):
        tag = self.tag_entry.get().strip()
        snippets = self.snippet_manager.get_snippets_by_tag(tag)
        if snippets:
            self.text_area.delete("1.0", tk.END)
            for snippet in snippets:
                self.text_area.insert(tk.END, f"{snippet.text}\n\n")
        else:
            messagebox.showinfo("Info", "No snippets found for this tag.")