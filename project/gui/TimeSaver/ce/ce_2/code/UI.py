import tkinter as tk
from tkinter import simpledialog, messagebox

class UI:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = None
        self.listbox = None

    def create_main_window(self) -> None:
        self.window = tk.Tk()
        self.window.title("Time Saver Application")

        self.listbox = tk.Listbox(self.window)
        self.listbox.pack()

        create_button = tk.Button(self.window, text="Create List", command=self.create_list)
        create_button.pack()

        edit_button = tk.Button(self.window, text="Edit List", command=self.edit_list)
        edit_button.pack()

        delete_button = tk.Button(self.window, text="Delete List", command=self.delete_list)
        delete_button.pack()

        self.display_lists(list(self.main_app.list_manager.list.keys()))

    def display_lists(self, lists: list) -> None:
        self.listbox.delete(0, tk.END)
        for list_name in lists:
            self.listbox.insert(tk.END, list_name)

    def create_list(self) -> None:
        name = simpledialog.askstring("Input", "Enter list name:")
        if name:
            self.main_app.list_manager.create_list(name)
            self.display_lists(list(self.main_app.list_manager.list.keys()))

    def edit_list(self) -> None:
        selected = self.listbox.curselection()
        if selected:
            old_name = self.listbox.get(selected[0])
            new_name = simpledialog.askstring("Input", "Enter new list name:", initialvalue=old_name)
            if new_name:
                self.main_app.list_manager.edit_list(old_name, new_name)
                self.display_lists(list(self.main_app.list_manager.list.keys()))

    def delete_list(self) -> None:
        selected = self.listbox.curselection()
        if selected:
            list_name = self.listbox.get(selected[0])
            self.main_app.list_manager.delete_list(list_name)
            self.display_lists(list(self.main_app.list_manager.list.keys()))

    def show_reminder_dialog(self, reminder: str) -> None:
        messagebox.showinfo("Reminder", reminder)