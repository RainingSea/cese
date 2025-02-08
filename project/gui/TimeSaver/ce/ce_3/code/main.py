import tkinter as tk
from tkinter import messagebox
from ShoppingListManager import ShoppingListManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Saver - Shopping List Manager")
        self.shopping_list_manager = ShoppingListManager("shopping_lists.txt")
        self.create_widgets()

    def create_widgets(self):
        self.list_name_entry = tk.Entry(self.root)
        self.list_name_entry.pack()

        self.create_button = tk.Button(self.root, text="Create List", command=self.create_list)
        self.create_button.pack()

        self.view_button = tk.Button(self.root, text="View Lists", command=self.view_lists)
        self.view_button.pack()

        self.item_entry = tk.Entry(self.root)
        self.item_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.list_display = tk.Text(self.root)
        self.list_display.pack()

    def create_list(self):
        list_name = self.list_name_entry.get()
        if list_name:
            self.shopping_list_manager.create_list(list_name)
            messagebox.showinfo("Success", f"List '{list_name}' created.")
        else:
            messagebox.showwarning("Warning", "Please enter a list name.")

    def view_lists(self):
        lists = self.shopping_list_manager.view_lists()
        self.list_display.delete(1.0, tk.END)
        for list_name in lists:
            self.list_display.insert(tk.END, f"{list_name}\n")

    def add_item(self):
        list_name = self.list_name_entry.get()
        item = self.item_entry.get()
        category = self.category_entry.get()
        if list_name and item and category:
            self.shopping_list_manager.add_item(list_name, item, category)
            messagebox.showinfo("Success", f"Item '{item}' added to '{list_name}'.")
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()