import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json
from tkinter import scrolledtext  # Importing scrolledtext for better text handling
import keyword  # Importing keyword for syntax highlighting

class SnippetManager:
    MAX_TAG_LENGTH = 20  # Maximum length for tags
    MAX_DESCRIPTION_LENGTH = 100  # Maximum length for descriptions

    def __init__(self):
        self.snippets = []
        self.load_snippets()

    def add_snippet(self, text: str, description: str, tags: list) -> None:
        if not text or not description or not tags:
            raise ValueError("Snippet text, description, and tags cannot be empty.")
        if any(len(tag) > self.MAX_TAG_LENGTH for tag in tags):
            raise ValueError(f"Tags must not exceed {self.MAX_TAG_LENGTH} characters.")
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must not exceed {self.MAX_DESCRIPTION_LENGTH} characters.")
        
        snippet = {"text": text, "description": description, "tags": tags}
        self.snippets.append(snippet)
        self.save_snippets()

    def edit_snippet(self, index: int, text: str, description: str, tags: list) -> None:
        if 0 <= index < len(self.snippets):
            if not text or not description or not tags:
                raise ValueError("Snippet text, description, and tags cannot be empty.")
            if any(len(tag) > self.MAX_TAG_LENGTH for tag in tags):
                raise ValueError(f"Tags must not exceed {self.MAX_TAG_LENGTH} characters.")
            if len(description) > self.MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description must not exceed {self.MAX_DESCRIPTION_LENGTH} characters.")
            
            self.snippets[index] = {"text": text, "description": description, "tags": tags}
            self.save_snippets()
        else:
            raise IndexError("Snippet index out of range.")

    def delete_snippet(self, index: int) -> None:
        if 0 <= index < len(self.snippets):
            del self.snippets[index]
            self.save_snippets()
        else:
            raise IndexError("Snippet index out of range.")

    def load_snippets(self) -> None:
        if os.path.exists('snippets.txt'):
            with open('snippets.txt', 'r') as file:
                for line in file:
                    text, description, tags = line.strip().split('|')
                    self.snippets.append({
                        "text": text,
                        "description": description,
                        "tags": tags.split(',')
                    })

    def save_snippets(self) -> None:
        with open('snippets.txt', 'w') as file:
            for snippet in self.snippets:
                file.write(f"{snippet['text']}|{snippet['description']}|{','.join(snippet['tags'])}\n")

    def filter_snippets(self, tag: str) -> list:
        return [snippet for snippet in self.snippets if tag in snippet['tags']]

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.root = tk.Tk()
        self.root.title("Snippet Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.text_input = scrolledtext.ScrolledText(self.root, height=10, width=50)  # Using ScrolledText for better usability
        self.text_input.pack()

        self.description_input = tk.Entry(self.root)
        self.description_input.pack()

        self.tag_input = tk.Entry(self.root)
        self.tag_input.pack()

        self.add_button = tk.Button(self.root, text="Add Snippet", command=self.add_snippet)
        self.add_button.pack()

        self.edit_button = tk.Button(self.root, text="Edit Snippet", command=self.edit_snippet)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Snippet", command=self.delete_snippet)
        self.delete_button.pack()

        self.display_area = scrolledtext.ScrolledText(self.root, height=10, width=50)  # Using ScrolledText for displaying snippets
        self.display_area.pack()

    def add_snippet(self):
        text = self.text_input.get("1.0", tk.END).strip()
        description = self.description_input.get().strip()
        tags = self.tag_input.get().strip().split(',')
        try:
            self.snippet_manager.add_snippet(text, description, tags)
            messagebox.showinfo("Success", "Snippet added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_snippet(self):
        index = simpledialog.askinteger("Input", "Enter snippet index to edit:")
        if index is not None:
            text = self.text_input.get("1.0", tk.END).strip()
            description = self.description_input.get().strip()
            tags = self.tag_input.get().strip().split(',')
            try:
                self.snippet_manager.edit_snippet(index, text, description, tags)
                messagebox.showinfo("Success", "Snippet edited successfully!")
            except (IndexError, ValueError) as e:
                messagebox.showerror("Error", str(e))

    def delete_snippet(self):
        index = simpledialog.askinteger("Input", "Enter snippet index to delete:")
        if index is not None:
            try:
                self.snippet_manager.delete_snippet(index)
                messagebox.showinfo("Success", "Snippet deleted successfully!")
            except IndexError as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    Main()