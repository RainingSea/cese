import tkinter as tk
from tkinter import simpledialog, messagebox
import os

class ShoppingList:
    def __init__(self, name: str) -> None:
        self.name = name
        self.items = {}

    def add_item(self, item: str, category: str) -> None:
        if category not in self.items:
            self.items[category] = []
        self.items[category].append(item)
        self.save_to_file()

    def import_items(self, previous_items: list) -> None:
        for item, category in previous_items:
            self.add_item(item, category)

    def save_to_file(self) -> None:
        with open(f"{self.name}.txt", "w") as file:
            for category, items in self.items.items():
                for item in items:
                    file.write(f"{item}|{category}\n")

class ShoppingPlanner:
    def __init__(self) -> None:
        self.list_of_lists = []

    def main(self) -> None:
        self.root = tk.Tk()
        self.root.title("Shopping Planner")
        self.root.geometry("400x400")
        
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.create_button = tk.Button(self.root, text="Create New List", command=self.create_shopping_list)
        self.create_button.pack(pady=10)

        self.load_shopping_lists()
        self.root.mainloop()

    def create_shopping_list(self) -> None:
        list_name = simpledialog.askstring("Input", "Enter shopping list name:")
        if list_name:
            shopping_list = ShoppingList(list_name)
            self.list_of_lists.append(shopping_list)
            self.listbox.insert(tk.END, list_name)

    def load_shopping_lists(self) -> None:
        for filename in os.listdir('.'):
            if filename.endswith('.txt'):
                list_name = filename[:-4]  # Remove .txt extension
                self.list_of_lists.append(ShoppingList(list_name))
                self.listbox.insert(tk.END, list_name)

if __name__ == "__main__":
    planner = ShoppingPlanner()
    planner.main()