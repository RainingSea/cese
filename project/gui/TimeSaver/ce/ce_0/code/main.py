import tkinter as tk
from shopping_list_manager import ShoppingListManager

class Main:
    def __init__(self):
        self.shopping_list_manager = ShoppingListManager()
        self.shopping_list_manager.load_lists()
        self.root = tk.Tk()
        self.root.title("Time Saver - Shopping List Manager")
        self.create_widgets()

    def create_widgets(self):
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack()

        self.listbox = tk.Listbox(self.list_frame)
        self.listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.add_button = tk.Button(self.root, text="Add List", command=self.add_list)
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete List", command=self.delete_list)
        self.delete_button.pack()

        self.update_listbox()

    def add_list(self):
        list_name = "New List"  # Placeholder for user input
        self.shopping_list_manager.create_list(list_name)
        self.update_listbox()

    def delete_list(self):
        selected_list = self.listbox.get(tk.ACTIVE)
        self.shopping_list_manager.delete_list(selected_list)
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for list_name in self.shopping_list_manager.list_of_lists:
            self.listbox.insert(tk.END, list_name)

    def main(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()