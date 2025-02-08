import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from theme import Theme

class TextEditor:
    def __init__(self) -> None:
        self.current_file = None
        self.theme = Theme().get_theme('default')
        self.root = tk.Tk()
        self.text_area = tk.Text(self.root, wrap='word', bg=self.theme.get('background', 'white'), fg=self.theme.get('foreground', 'black'))
        self.text_area.pack(expand=True, fill='both')
        self.create_menu()
        self.root.mainloop()

    def create_menu(self) -> None:
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.create_new_file)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save', command=self.save_file)

    def create_new_file(self) -> None:
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self, file_path: str = None) -> None:
        if file_path is None:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path

    def save_file(self, file_path: str = None) -> None:
        if file_path is None:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                self.current_file = file_path