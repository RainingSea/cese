import tkinter as tk
from tkinter import filedialog, messagebox
from text_area import TextArea

class NotepadPlus:
    def __init__(self):
        self.current_file = None
        self.theme = "light"  # Default theme
        self.text_area = TextArea()
        self.root = tk.Tk()
        self.root.title("Notepad Plus")
        self.create_widgets()

    def create_widgets(self):
        self.text_widget = tk.Text(self.root)
        self.text_widget.pack(expand=True, fill='both')

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)

        self.root.mainloop()

    def create_new_file(self):
        self.text_area.content = ""
        self.text_widget.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self, file_path: str = None):
        if file_path is None:
            file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, self.text_area.content)
                self.current_file = file_path

    def save_file(self, file_path: str = None):
        if file_path is None:
            if self.current_file:
                file_path = self.current_file
            else:
                file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get_content())
                self.current_file = file_path

    def save_as(self):
        self.save_file()

    def search(self, query: str):
        content = self.text_area.get_content()
        if query in content:
            messagebox.showinfo("Search", f"'{query}' found.")
        else:
            messagebox.showinfo("Search", f"'{query}' not found.")

    def replace(self, old_text: str, new_text: str):
        self.text_area.content = self.text_area.content.replace(old_text, new_text)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.text_area.content)

    def set_theme(self, theme: str):
        self.theme = theme
        # Theme setting logic can be implemented here

if __name__ == "__main__":
    NotepadPlus()