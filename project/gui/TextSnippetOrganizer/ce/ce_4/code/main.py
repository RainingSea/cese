import tkinter as tk
from tkinter import messagebox, simpledialog
from snippets.snippet_manager import SnippetManager

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.snippet_manager.load_snippets()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Snippet Manager")
        
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        self.add_button = tk.Button(self.root, text="Add Snippet", command=self.add_snippet)
        self.add_button.pack(side=tk.LEFT)
        
        self.edit_button = tk.Button(self.root, text="Edit Snippet", command=self.edit_snippet)
        self.edit_button.pack(side=tk.LEFT)
        
        self.delete_button = tk.Button(self.root, text="Delete Snippet", command=self.delete_snippet)
        self.delete_button.pack(side=tk.LEFT)

        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for tag in self.snippet_manager.snippets.keys():
            self.listbox.insert(tk.END, tag)

    def add_snippet(self):
        content = simpledialog.askstring("Content", "Enter snippet content:")
        tags = simpledialog.askstring("Tags", "Enter tags (comma separated):").split(',')
        description = simpledialog.askstring("Description", "Enter description:")
        self.snippet_manager.add_snippet(content, tags, description)
        self.update_listbox()

    def edit_snippet(self):
        selected_tag = self.listbox.get(tk.ACTIVE)
        if not selected_tag:
            messagebox.showwarning("Edit Snippet", "Select a snippet to edit.")
            return
        content = simpledialog.askstring("Content", "Enter new snippet content:")
        tags = simpledialog.askstring("Tags", "Enter new tags (comma separated):").split(',')
        description = simpledialog.askstring("Description", "Enter new description:")
        self.snippet_manager.edit_snippet(selected_tag, content, tags, description)
        self.update_listbox()

    def delete_snippet(self):
        selected_tag = self.listbox.get(tk.ACTIVE)
        if not selected_tag:
            messagebox.showwarning("Delete Snippet", "Select a snippet to delete.")
            return
        self.snippet_manager.delete_snippet(selected_tag)
        self.update_listbox()

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()