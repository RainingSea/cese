import tkinter as tk
from tkinter import messagebox
from shopping_planner import ShoppingPlanner

class UserInterface:
    def __init__(self, planner: ShoppingPlanner):
        self.planner = planner
        self.root = tk.Tk()
        self.create_main_window()

    def create_main_window(self):
        self.root.title("Shopping Planner")

        self.list_name_entry = tk.Entry(self.root)
        self.list_name_entry.pack()

        self.item_entry = tk.Entry(self.root)
        self.item_entry.pack()

        self.category_var = tk.StringVar(self.root)
        self.category_var.set(self.planner.categories[0] if self.planner.categories else "No Categories")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.planner.categories)
        self.category_menu.pack()

        self.add_item_button = tk.Button(self.root, text="Add Item", command=self.add_item_button_clicked)
        self.add_item_button.pack()

        self.save_list_button = tk.Button(self.root, text="Save List", command=self.save_list_button_clicked)
        self.save_list_button.pack()

        self.import_items_button = tk.Button(self.root, text="Import Items", command=self.import_items_button_clicked)
        self.import_items_button.pack()

        self.shopping_list_display = tk.Text(self.root)
        self.shopping_list_display.pack()

        self.load_shopping_lists()

    def add_item_button_clicked(self):
        list_name = self.list_name_entry.get()
        item = self.item_entry.get()
        category = self.category_var.get()
        self.planner.add_item_to_list(list_name, item, category)
        self.update_display(list_name)

    def save_list_button_clicked(self):
        list_name = self.list_name_entry.get()
        self.planner.save_list_to_file(list_name)
        messagebox.showinfo("Info", f"List '{list_name}' saved successfully!")

    def import_items_button_clicked(self):
        list_name = self.list_name_entry.get()
        source_list = self.item_entry.get()  # Assuming item entry is used for source list name
        self.planner.import_items_from_list(list_name, source_list)
        self.update_display(list_name)

    def update_display(self, list_name):
        self.shopping_list_display.delete(1.0, tk.END)
        if list_name in self.planner.shopping_lists:
            for item in self.planner.shopping_lists[list_name]:
                self.shopping_list_display.insert(tk.END, f"{item}\n")

    def load_shopping_lists(self):
        self.planner.load_lists_from_file()