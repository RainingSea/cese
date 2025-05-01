import tkinter as tk
from tkinter import messagebox
from typing import List
import os

class Item:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

class ShoppingList:
    def __init__(self, name: str):
        self.name = name
        self.items: List[Item] = []

    def add_item(self, item: str, category: str) -> None:
        new_item = Item(item, category)
        self.items.append(new_item)

    def load_previous_lists(self) -> List[Item]:
        previous_items = []
        try:
            with open('previous_lists.txt', 'r') as file:
                for line in file:
                    name, category = line.strip().split('|')
                    previous_items.append(Item(name, category))
        except FileNotFoundError:
            messagebox.showerror("Error", "Previous lists file not found.")
        return previous_items

class ShoppingListManager:
    def __init__(self):
        self.list_of_lists: List[ShoppingList] = []

    def create_list(self, name: str) -> None:
        shopping_list = ShoppingList(name)
        self.list_of_lists.append(shopping_list)

    def add_item(self, list_name: str, item_name: str, category: str) -> None:
        shopping_list = self._find_list(list_name)
        if shopping_list:
            if item_name and category:
                shopping_list.add_item(item_name, category)
            else:
                messagebox.showwarning("Input Error", "Item name and category cannot be empty.")
        else:
            messagebox.showerror("Error", "Shopping list not found.")

    def remove_item(self, list_name: str, item_name: str) -> None:
        shopping_list = self._find_list(list_name)
        if shopping_list:
            item_to_remove = next((item for item in shopping_list.items if item.name == item_name), None)
            if item_to_remove:
                shopping_list.items.remove(item_to_remove)
            else:
                messagebox.showerror("Error", "Item not found in the list.")
        else:
            messagebox.showerror("Error", "Shopping list not found.")

    def edit_item(self, list_name: str, old_item_name: str, new_item_name: str) -> None:
        shopping_list = self._find_list(list_name)
        if shopping_list:
            item_to_edit = next((item for item in shopping_list.items if item.name == old_item_name), None)
            if item_to_edit:
                item_to_edit.name = new_item_name
            else:
                messagebox.showerror("Error", "Item not found in the list.")
        else:
            messagebox.showerror("Error", "Shopping list not found.")

    def import_items(self, list_name: str) -> None:
        shopping_list = self._find_list(list_name)
        if shopping_list:
            previous_items = shopping_list.load_previous_lists()
            for item in previous_items:
                shopping_list.add_item(item.name, item.category)
        else:
            messagebox.showerror("Error", "Shopping list not found.")

    def _find_list(self, name: str) -> ShoppingList:
        return next((lst for lst in self.list_of_lists if lst.name == name), None)

class Main:
    def __init__(self):
        self.shopping_list_manager = ShoppingListManager()

    def main(self) -> None:
        self._load_data()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Shopping List Manager")

        self.list_name_entry = tk.Entry(self.root)
        self.list_name_entry.pack()

        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        add_button = tk.Button(self.root, text="Add Item", command=self._add_item)
        add_button.pack()

        import_button = tk.Button(self.root, text="Import Previous Items", command=self._import_previous_items)
        import_button.pack()

        self.root.mainloop()

    def _add_item(self) -> None:
        list_name = self.list_name_entry.get()
        item_name = self.item_name_entry.get()
        category = self.category_entry.get()
        if item_name and category:
            self.shopping_list_manager.add_item(list_name, item_name, category)
            self.list_name_entry.delete(0, tk.END)
            self.item_name_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill in both item name and category.")

    def _import_previous_items(self) -> None:
        list_name = self.list_name_entry.get()
        if list_name:
            self.shopping_list_manager.import_items(list_name)
        else:
            messagebox.showwarning("Input Error", "Please enter a shopping list name.")

    def _load_data(self) -> None:
        if os.path.exists('shopping_lists.txt'):
            with open('shopping_lists.txt', 'r') as file:
                for line in file:
                    list_name = line.strip()
                    self.shopping_list_manager.create_list(list_name)

if __name__ == "__main__":
    app = Main()
    app.main()