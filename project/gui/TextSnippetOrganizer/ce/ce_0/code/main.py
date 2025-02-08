import tkinter as tk
from tkinter import messagebox
from snippet_manager import SnippetManager

class Main:
    def __init__(self):
        self.snippet_manager = SnippetManager()
        self.root = tk.Tk()
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Snippet Manager")

        self.text_area = tk.Text(self.root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)

        self.tag_input = tk.Entry(self.root)
        self.tag_input.pack(padx=10, pady=5)

        self.description_input = tk.Entry(self.root)
        self.description_input.pack(padx=10, pady=5)

        self.save_button = tk.Button(self.root, text="Save Snippet", command=self.save_snippet)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(self.root, text="Load Snippets", command=self.load_snippets)
        self.load_button.pack(pady=5)

    def save_snippet(self):
        content = self.text_area.get("1.0", tk.END).strip()
        tags = self.tag_input.get().strip().split(',')
        description = self.description_input.get().strip()

        if content and tags and description:
            snippet = Snippet(content, tags, description)
            self.snippet_manager.save_snippet(snippet)
            messagebox.showinfo("Success", "Snippet saved successfully!")
            self.clear_inputs()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def load_snippets(self):
        self.snippet_manager.load_snippets()
        messagebox.showinfo("Load Success", "Snippets loaded successfully!")

    def clear_inputs(self):
        self.text_area.delete("1.0", tk.END)
        self.tag_input.delete(0, tk.END)
        self.description_input.delete(0, tk.END)

if __name__ == "__main__":
    Main()