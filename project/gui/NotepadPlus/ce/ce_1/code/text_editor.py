import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter

class TextEditor:
    def __init__(self):
        self.current_file = ""
        self.theme = "default"
        self.root = tk.Tk()
        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=1, fill='both')
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = ""

    def open_file(self, filename: str = None):
        if filename is None:
            filename = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = filename

    def save_file(self, filename: str = None):
        if filename is None:
            filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                self.current_file = filename

    def search(self, query: str) -> list:
        content = self.text_area.get(1.0, tk.END)
        matches = []
        start_index = '1.0'
        while True:
            start_index = self.text_area.search(query, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(query)}c"
            matches.append((start_index, end_index))
            start_index = end_index
        return matches

    def replace(self, old_text: str, new_text: str) -> None:
        content = self.text_area.get(1.0, tk.END)
        updated_content = content.replace(old_text, new_text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, updated_content)

    def set_theme(self, theme: str) -> None:
        self.theme = theme
        # Implement theme setting logic here

    def run(self):
        self.root.mainloop()