import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Menu
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter

class NotepadPlus:
    def __init__(self):
        self.root = tk.Tk()
        self.text_area = TextArea(self)
        self.menu_bar = MenuBar(self)
        self.theme_manager = ThemeManager()
        self.root.config(menu=self.menu_bar)
        self.root.title("Notepad Plus")
        self.root.geometry("800x600")
        self.root.mainloop()

    def create_new_file(self):
        self.text_area.set_content("")

    def open_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.set_content(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self, file_path: str):
        try:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get_content())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def search_text(self, query: str):
        content = self.text_area.get_content()
        if query in content:
            messagebox.showinfo("Search Result", f"'{query}' found in the text.")
        else:
            messagebox.showinfo("Search Result", f"'{query}' not found in the text.")

    def replace_text(self, old_text: str, new_text: str):
        content = self.text_area.get_content().replace(old_text, new_text)
        self.text_area.set_content(content)

    def change_theme(self, theme_name: str):
        self.theme_manager.apply_theme(theme_name)

class TextArea:
    def __init__(self, parent: NotepadPlus):
        self.text_widget = tk.Text(parent.root, wrap='word')
        self.text_widget.pack(expand=1, fill='both')
        self.highlight_syntax()

    def highlight_syntax(self):
        content = self.get_content()
        highlighted_content = highlight(content, PythonLexer(), TkinterFormatter())
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, highlighted_content)

    def get_content(self) -> str:
        return self.text_widget.get(1.0, tk.END)

    def set_content(self, content: str):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, content)
        self.highlight_syntax()

class MenuBar:
    def __init__(self, parent: NotepadPlus):
        self.notepad = parent
        self.create_file_menu()
        self.create_edit_menu()
        self.create_theme_menu()

    def create_file_menu(self):
        file_menu = Menu(self.notepad.root)
        file_menu.add_command(label="New", command=self.notepad.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file_dialog)
        file_menu.add_command(label="Save", command=self.save_file_dialog)
        self.notepad.root.menu.add_cascade(label="File", menu=file_menu)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.notepad.open_file(file_path)

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.notepad.save_file(file_path)

    def create_edit_menu(self):
        edit_menu = Menu(self.notepad.root)
        edit_menu.add_command(label="Search", command=self.search_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        self.notepad.root.menu.add_cascade(label="Edit", menu=edit_menu)

    def search_text(self):
        query = simpledialog.askstring("Search", "Enter text to search:")
        if query:
            self.notepad.search_text(query)

    def replace_text(self):
        old_text = simpledialog.askstring("Replace", "Enter text to replace:")
        if old_text:
            new_text = simpledialog.askstring("Replace", "Enter new text:")
            if new_text:
                self.notepad.replace_text(old_text, new_text)

    def create_theme_menu(self):
        theme_menu = Menu(self.notepad.root)
        theme_menu.add_command(label="Light", command=lambda: self.notepad.change_theme("light"))
        theme_menu.add_command(label="Dark", command=lambda: self.notepad.change_theme("dark"))
        self.notepad.root.menu.add_cascade(label="Themes", menu=theme_menu)

class ThemeManager:
    def __init__(self):
        self.themes = {
            "light": {"bg": "white", "fg": "black"},
            "dark": {"bg": "black", "fg": "white"}
        }

    def apply_theme(self, theme_name: str):
        theme = self.themes.get(theme_name)
        if theme:
            for widget in self.root.winfo_children():
                widget.config(bg=theme["bg"], fg=theme["fg"])

if __name__ == "__main__":
    NotepadPlus()