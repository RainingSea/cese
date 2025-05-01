import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter

class Main:
    def main(self) -> str:
        self.root = tk.Tk()
        self.root.title("Notepad Plus")
        self.text_editor = TextEditor(self.root)
        self.root.mainloop()

class TextEditor:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.content = ""
        self.file_path = ""
        self.text_area = tk.Text(master, wrap='word')
        self.text_area.pack(expand=1, fill='both')
        self.create_menu()
        self.create_buttons()

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=menu_bar)

    def create_buttons(self) -> None:
        search_button = tk.Button(self.master, text="Search", command=self.search)
        search_button.pack(side='left')
        replace_button = tk.Button(self.master, text="Replace", command=self.replace)
        replace_button.pack(side='left')

    def create_new_file(self) -> None:
        self.text_area.delete(1.0, tk.END)
        self.file_path = ""

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.content)
                self.file_path = file_path

    def save_file(self) -> None:
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def search(self) -> None:
        query = simpledialog.askstring("Search", "Enter text to search:")
        if query:
            content = self.text_area.get(1.0, tk.END)
            if re.search(query, content):
                messagebox.showinfo("Search Result", f"'{query}' found!")
            else:
                messagebox.showinfo("Search Result", f"'{query}' not found!")

    def replace(self) -> None:
        old_text = simpledialog.askstring("Replace", "Enter text to replace:")
        new_text = simpledialog.askstring("Replace", "Enter new text:")
        content = self.text_area.get(1.0, tk.END)
        updated_content = content.replace(old_text, new_text)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, updated_content)

    def apply_syntax_highlighting(self, language: str) -> None:
        if language == "Python":
            lexer = PythonLexer()
            formatter = TkinterFormatter()
            highlighted_code = highlight(self.text_area.get(1.0, tk.END), lexer, formatter)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, highlighted_code)

    def set_theme(self, theme: str) -> None:
        # Theme setting logic will be implemented later
        pass

if __name__ == "__main__":
    app = Main()
    app.main()