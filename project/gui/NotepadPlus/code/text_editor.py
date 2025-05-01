import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter
from theme_manager import ThemeManager

class TextEditor:
    def __init__(self, master):
        self.master = master
        self.theme_manager = ThemeManager()
        self.current_file = None
        self.text_area = tk.Text(master, wrap='word')
        self.text_area.pack(expand=True, fill='both')
        self.create_menu()
        self.theme_manager.load_themes()
        self.apply_theme("default")

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Search", command=self.search)
        edit_menu.add_command(label="Replace", command=self.replace)
        edit_menu.add_command(label="Indent", command=self.indent_code)
        edit_menu.add_command(label="Dedent", command=self.dedent_code)

    def create_new_file(self) -> None:
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"),
                                                           ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path
                self.apply_syntax_highlighting()

    def save_file(self) -> None:
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                       filetypes=[("Text files", "*.txt"),
                                                                  ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END).strip())
                    self.current_file = file_path

    def search(self) -> None:
        query = simpledialog.askstring("Search", "Enter text to search:")
        if query is not None:
            content = self.text_area.get(1.0, tk.END)
            if query in content:
                messagebox.showinfo("Search Result", f"'{query}' found!")
            else:
                messagebox.showinfo("Search Result", f"'{query}' not found!")

    def replace(self) -> None:
        old_text = simpledialog.askstring("Replace", "Enter text to replace:")
        if old_text is not None:
            new_text = simpledialog.askstring("Replace", "Enter new text:")
            if new_text is not None:
                content = self.text_area.get(1.0, tk.END)
                new_content = content.replace(old_text, new_text)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, new_content)
                self.apply_syntax_highlighting()
            else:
                messagebox.showwarning("Input Error", "Replacement text cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "Text to replace cannot be empty.")

    def apply_theme(self, theme_name: str) -> None:
        theme = self.theme_manager.get_theme(theme_name)
        self.text_area.config(bg=theme['background'], fg=theme['foreground'])

    def apply_syntax_highlighting(self) -> None:
        content = self.text_area.get(1.0, tk.END)
        lexer = PythonLexer()
        formatter = TkinterFormatter()
        highlighted_content = highlight(content, lexer, formatter)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, highlighted_content)

    def indent_code(self) -> None:
        self.modify_indentation(4)

    def dedent_code(self) -> None:
        self.modify_indentation(-4)

    def modify_indentation(self, spaces: int) -> None:
        current_selection = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST) if self.text_area.tag_ranges(tk.SEL) else self.text_area.get(1.0, tk.END)
        lines = current_selection.split('\n')
        for i in range(len(lines)):
            if spaces > 0:
                lines[i] = ' ' * spaces + lines[i]
            else:
                lines[i] = lines[i].lstrip(' ' * abs(spaces))
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_area.insert(tk.END, '\n'.join(lines))