import tkinter as tk
from tkinter import filedialog, messagebox
from theme_manager import ThemeManager
from syntax_highlighter import SyntaxHighlighter

class NotepadPlus:
    def __init__(self):
        self.current_file = None
        self.themes = ThemeManager()
        self.syntax_highlighter = SyntaxHighlighter()
        self.init_ui()

    def init_ui(self):
        self.root = tk.Tk()
        self.root.title("Notepad Plus")
        self.text_area = tk.Text(self.root)
        self.text_area.pack(expand=True, fill='both')

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

        self.root.mainloop()

    def create_new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self, filename=None):
        if filename is None:
            filename = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.current_file = filename

    def save_file(self, filename=None):
        if filename is None:
            filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.current_file = filename

    def search_text(self, query: str) -> list:
        content = self.text_area.get(1.0, tk.END)
        return [line for line in content.splitlines() if query in line]

    def replace_text(self, old_text: str, new_text: str) -> None:
        content = self.text_area.get(1.0, tk.END)
        new_content = content.replace(old_text, new_text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, new_content)

    def apply_theme(self, theme_name: str) -> None:
        theme = self.themes.get_theme(theme_name)
        self.text_area.config(bg=theme["background"], fg=theme["foreground"], font=theme["font"])

if __name__ == "__main__":
    NotepadPlus()