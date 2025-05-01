import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter
from theme import Theme

class TextEditor:
    def __init__(self, master):
        self.master = master
        self.content = ""
        self.text_area = tk.Text(master)
        self.text_area.pack(expand=True, fill='both')
        self.create_menu()
        self.theme = Theme()
        self.theme.load_theme()

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=menu_bar)

    def create_new_file(self) -> None:
        self.text_area.delete(1.0, tk.END)

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.content)

    def save_file(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                self.content = self.text_area.get(1.0, tk.END)
                file.write(self.content)

    def search(self, query: str) -> list:
        indices = []
        start = '1.0'
        while True:
            start = self.text_area.search(query, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(query)}c"
            indices.append(start)
            start = end
        return indices

    def replace(self, old_text: str, new_text: str) -> None:
        content = self.text_area.get(1.0, tk.END)
        new_content = content.replace(old_text, new_text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, new_content)

    def apply_theme(self, theme: str) -> None:
        # Placeholder for theme application logic
        pass