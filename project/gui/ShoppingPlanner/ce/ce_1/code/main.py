import tkinter as tk
from tkinter import messagebox, simpledialog
from shopping_list import ShoppingList

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shopping List Manager")
        self.current_list = ShoppingList()

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New List", command=self.create_list)
        self.file_menu.add_command(label="Import Items", command=self.import_items)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.entry_name = tk.Entry(self.master)
        self.entry_name.pack(side=tk.LEFT, padx=5)

        self.entry_category = tk.Entry(self.master)
        self.entry_category.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.master, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

    def create_list(self) -> None:
        self.current_list = ShoppingList()
        self.listbox.delete(0, tk.END)

    def add_item(self) -> None:
        name = self.entry_name.get()
        category = self.entry_category.get()
        if name and category:
            self.current_list.add_item(name, category)
            self.listbox.insert(tk.END, f"{name} ({category})")
            self.entry_name.delete(0, tk.END)
            self.entry_category.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both name and category.")

    def import_items(self) -> None:
        file_path = simpledialog.askstring("Import Items", "Enter the file path:")
        if file_path:
            self.current_list.import_items(file_path)
            self.listbox.delete(0, tk.END)
            for item in self.current_list.get_items():
                self.listbox.insert(tk.END, f"{item[0]} ({item[1]})")

    def save_list(self) -> None:
        self.current_list.save_to_file('shopping_lists.txt')

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()