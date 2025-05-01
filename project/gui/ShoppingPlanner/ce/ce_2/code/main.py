import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import filedialog

class ShoppingList:
    def __init__(self):
        self.items = []
        self.categories = []

    def add_item(self, item: str, category: str) -> None:
        self.items.append((item, category))
        if category not in self.categories:
            self.categories.append(category)

    def import_items(self, previous_list: str) -> None:
        try:
            with open(previous_list, 'r') as file:
                for line in file:
                    item, category = line.strip().split('|')
                    self.add_item(item, category)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import items: {e}")

    def save_list(self) -> None:
        with open('shopping_lists.txt', 'a') as file:
            for item, category in self.items:
                file.write(f"{item}|{category}\n")

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_list = ShoppingList()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.root.title("Shopping Planner")
        self.root.geometry("400x400")

        self.list_display = tk.Text(self.root, height=15, width=50)
        self.list_display.pack()

        self.add_item_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_item_button.pack()

        self.create_list_button = tk.Button(self.root, text="Create New List", command=self.create_list)
        self.create_list_button.pack()

        self.import_list_button = tk.Button(self.root, text="Import List", command=self.import_list)
        self.import_list_button.pack()

    def add_item(self) -> None:
        item = simpledialog.askstring("Input", "Enter item name:")
        category = simpledialog.askstring("Input", "Enter item category:")
        if item and category:
            self.current_list.add_item(item, category)
            self.update_display()

    def create_list(self) -> None:
        self.current_list = ShoppingList()
        self.update_display()

    def import_list(self) -> None:
        file_path = filedialog.askopenfilename(title="Select a shopping list", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.current_list.import_items(file_path)
            self.update_display()

    def update_display(self) -> None:
        self.list_display.delete(1.0, tk.END)
        for item, category in self.current_list.items:
            self.list_display.insert(tk.END, f"{item} | {category}\n")

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()