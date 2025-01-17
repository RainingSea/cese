import tkinter as tk
from tkinter import messagebox
from list_manager import ListManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Saver Application")
        self.list_manager = ListManager()
        self.create_widgets()

    def create_widgets(self):
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack()

        self.list_label = tk.Label(self.list_frame, text="Shopping Lists:")
        self.list_label.pack()

        self.listbox = tk.Listbox(self.list_frame)
        self.listbox.pack()

        self.add_list_entry = tk.Entry(self.list_frame)
        self.add_list_entry.pack()

        self.add_list_button = tk.Button(self.list_frame, text="Add List", command=self.add_list)
        self.add_list_button.pack()

        self.load_lists()

    def load_lists(self):
        self.listbox.delete(0, tk.END)
        for shopping_list in self.list_manager.shopping_lists:
            self.listbox.insert(tk.END, shopping_list)

    def add_list(self):
        list_name = self.add_list_entry.get()
        if list_name:
            self.list_manager.create_list(list_name)
            self.load_lists()
            self.add_list_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a list name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()