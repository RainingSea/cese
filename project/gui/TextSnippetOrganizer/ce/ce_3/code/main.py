import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from snippets.snippet_manager import SnippetManager
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Snippet Manager")
        self.snippet_manager = SnippetManager()

        self.create_widgets()
        self.load_snippets()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap='word', height=15)
        self.text_area.pack()

        self.tag_entry = tk.Entry(self.root)
        self.tag_entry.pack()

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.save_button = tk.Button(self.root, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack()

        self.listbox = Listbox(self.root)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def save_snippet(self):
        tag = self.tag_entry.get()
        snippet = self.text_area.get("1.0", tk.END).strip()
        description = self.description_entry.get()

        if tag and snippet:
            self.snippet_manager.save_snippet(tag, snippet, description)
            self.load_snippets()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Tag and Snippet cannot be empty.")

    def load_snippets(self):
        self.listbox.delete(0, tk.END)
        snippets = self.snippet_manager.list_snippets()
        for snippet in snippets:
            self.listbox.insert(tk.END, snippet)

    def on_select(self, event):
        selected_tag = self.listbox.get(self.listbox.curselection())
        snippet_data = self.snippet_manager.retrieve_snippet(selected_tag)
        if snippet_data:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, snippet_data['snippet'])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, snippet_data['description'])

    def clear_entries(self):
        self.tag_entry.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
        self.description_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()