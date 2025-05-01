import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from snippet_manager import SnippetManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Snippet Organizer")
        self.snippet_manager = SnippetManager()
        self.create_widgets()
        self.load_snippets()

    def create_widgets(self):
        self.text_area = tk.Text(self.master, height=10, width=50)
        self.text_area.pack()

        self.tag_entry = tk.Entry(self.master)
        self.tag_entry.pack()
        self.tag_entry.insert(0, "Enter tags (comma separated)")

        self.description_entry = tk.Entry(self.master)
        self.description_entry.pack()
        self.description_entry.insert(0, "Enter description")

        self.save_button = tk.Button(self.master, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack()

        self.search_button = tk.Button(self.master, text="Search Snippet", command=self.search_snippet)
        self.search_button.pack()

        self.snippet_listbox = Listbox(self.master)
        self.snippet_listbox.pack()

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.snippet_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.snippet_listbox.yview)

    def save_snippet(self):
        snippet_text = self.text_area.get("1.0", tk.END).strip()
        tags = self.tag_entry.get().strip().split(',')
        description = self.description_entry.get().strip()
        
        if snippet_text and tags:
            self.snippet_manager.add_snippet(snippet_text, tags, description)
            self.text_area.delete("1.0", tk.END)
            self.tag_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.update_snippet_listbox()
        else:
            messagebox.showwarning("Input Error", "Snippet text and tags cannot be empty.")

    def search_snippet(self):
        tag = self.tag_entry.get().strip()
        if tag:
            snippets = self.snippet_manager.search_snippets(tag)
            self.snippet_listbox.delete(0, tk.END)
            for snippet in snippets:
                self.snippet_listbox.insert(tk.END, snippet.text)
        else:
            messagebox.showwarning("Input Error", "Tag cannot be empty.")

    def load_snippets(self):
        self.snippet_manager.load_snippets()
        self.update_snippet_listbox()

    def update_snippet_listbox(self):
        self.snippet_listbox.delete(0, tk.END)
        for snippet in self.snippet_manager.snippets:
            self.snippet_listbox.insert(tk.END, snippet.text)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()