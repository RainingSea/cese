import tkinter as tk
from tkinter import messagebox
from shopping_list_manager import ShoppingListManager

class Main:
    def __init__(self):
        self.shopping_list_manager = ShoppingListManager('shopping_lists.txt', 'categories.txt')
        self.root = tk.Tk()
        self.root.title("Shopping Planner")
        self.create_widgets()

    def create_widgets(self):
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack()

        self.list_name_entry = tk.Entry(self.list_frame)
        self.list_name_entry.pack(side=tk.LEFT)

        self.add_list_button = tk.Button(self.list_frame, text="Create List", command=self.create_list)
        self.add_list_button.pack(side=tk.LEFT)

        self.item_frame = tk.Frame(self.root)
        self.item_frame.pack()

        self.item_name_entry = tk.Entry(self.item_frame)
        self.item_name_entry.pack(side=tk.LEFT)

        self.category_entry = tk.Entry(self.item_frame)
        self.category_entry.pack(side=tk.LEFT)

        self.add_item_button = tk.Button(self.item_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(side=tk.LEFT)

        self.import_button = tk.Button(self.root, text="Import Items", command=self.import_items)
        self.import_button.pack()

        self.list_display = tk.Text(self.root)
        self.list_display.pack()

    def create_list(self):
        list_name = self.list_name_entry.get()
        self.shopping_list_manager.create_list(list_name)
        self.list_name_entry.delete(0, tk.END)
        self.update_list_display()

    def add_item(self):
        list_name = self.list_name_entry.get()
        item_name = self.item_name_entry.get()
        category = self.category_entry.get()
        self.shopping_list_manager.add_item(list_name, item_name, category)
        self.item_name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.update_list_display()

    def import_items(self):
        list_name = self.list_name_entry.get()
        items = self.shopping_list_manager.import_items(list_name)
        if items:
            messagebox.showinfo("Imported Items", "\n".join([f"{item[0]} ({item[1]})" for item in items]))
        else:
            messagebox.showwarning("Warning", "No items found for this list.")

    def update_list_display(self):
        self.list_display.delete(1.0, tk.END)
        for list_name, items in self.shopping_list_manager.lists.items():
            item_strings = [f"{item.name} ({item.category})" for item in items]
            self.list_display.insert(tk.END, f"{list_name}: {', '.join(item_strings)}\n")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()