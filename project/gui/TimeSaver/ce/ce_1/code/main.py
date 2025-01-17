import tkinter as tk
from tkinter import messagebox
from shopping_list_manager import ShoppingListManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Shopping List Manager")
        self.list_manager = ShoppingListManager()

        self.create_widgets()

    def create_widgets(self):
        self.new_list_button = tk.Button(self.master, text="New Shopping List", command=self.create_new_list)
        self.new_list_button.pack()

        self.view_lists_button = tk.Button(self.master, text="View Existing Lists", command=self.view_existing_lists)
        self.view_lists_button.pack()

    def create_new_list(self):
        list_name = tk.simpledialog.askstring("Input", "Enter the name of the new shopping list:")
        if list_name:
            self.list_manager.create_list(list_name)
            messagebox.showinfo("Success", f"Shopping list '{list_name}' created!")

    def view_existing_lists(self):
        lists = self.list_manager.load_lists()
        messagebox.showinfo("Existing Lists", "\n".join(lists))

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()