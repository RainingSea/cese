import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List

class Item:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

class ShoppingList:
    def __init__(self):
        self.items = []

    def add_item(self, item: str, category: str):
        self.items.append(Item(item, category))

    def remove_item(self, item: str):
        self.items = [i for i in self.items if i.name != item]

    def save_list(self):
        with open('shopping_lists.txt', 'a') as file:
            for item in self.items:
                file.write(f"{item.name},{item.category}\n")

    def load_previous_lists(self) -> List[Item]:
        previous_items = []
        try:
            with open('previous_lists.txt', 'r') as file:
                for line in file:
                    name, category = line.strip().split(',')
                    previous_items.append(Item(name, category))
        except FileNotFoundError:
            messagebox.showerror("Error", "Previous lists file not found.")
        return previous_items

class Main:
    def __init__(self, root):
        self.root = root
        self.current_list = ShoppingList()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Shopping Planner")
        
        self.item_entry = tk.Entry(self.root)
        self.item_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.save_button = tk.Button(self.root, text="Save List", command=self.save_list)
        self.save_button.pack()

        self.import_button = tk.Button(self.root, text="Import Previous List", command=self.import_previous_list)
        self.import_button.pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

    def add_item(self):
        item_name = self.item_entry.get()
        category_name = self.category_entry.get()
        if item_name and category_name:
            self.current_list.add_item(item_name, category_name)
            self.listbox.insert(tk.END, f"{item_name} ({category_name})")
            self.item_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both item and category.")

    def save_list(self):
        self.current_list.save_list()
        messagebox.showinfo("Success", "Shopping list saved successfully.")

    def import_previous_list(self):
        previous_items = self.current_list.load_previous_lists()
        for item in previous_items:
            self.current_list.add_item(item.name, item.category)
            self.listbox.insert(tk.END, f"{item.name} ({item.category})")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()