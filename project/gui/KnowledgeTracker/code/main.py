import tkinter as tk
from tkinter import messagebox, simpledialog
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Knowledge Tracker")
        self.knowledge_manager = KnowledgeManager()
        
        self.category_var = tk.StringVar(value="theories")
        self.search_var = tk.StringVar()

        self.create_widgets()
        self.load_entries()

    def create_widgets(self):
        self.entry_text = tk.Text(self.root, height=10, width=50)
        self.entry_text.pack()

        self.category_menu = tk.OptionMenu(self.root, self.category_var, "theories", "concepts", "experiments", command=self.load_entries)
        self.category_menu.pack()

        self.add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.pack()

        self.update_button = tk.Button(self.root, text="Update Entry", command=self.update_entry)
        self.update_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Entry", command=self.delete_entry)
        self.delete_button.pack()

        self.search_entry = tk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.search_entries)

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack()

    def load_entries(self):
        self.listbox.delete(0, tk.END)
        category = self.category_var.get()
        entries = self.knowledge_manager.load_entries(category)
        for entry in entries:
            self.listbox.insert(tk.END, entry)

    def add_entry(self):
        entry = self.entry_text.get("1.0", tk.END).strip()
        category = self.category_var.get()
        if entry:
            self.knowledge_manager.save_entry(entry, category)
            self.load_entries()
            self.entry_text.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Input Error", "Entry cannot be empty.")

    def update_entry(self):
        selected_entry = self.listbox.get(tk.ACTIVE)
        if selected_entry:
            new_entry = simpledialog.askstring("Update Entry", "Update your entry:", initialvalue=selected_entry)
            if new_entry:
                category = self.category_var.get()
                self.knowledge_manager.update_entry(selected_entry, new_entry, category)
                self.load_entries()
        else:
            messagebox.showwarning("Selection Error", "No entry selected.")

    def delete_entry(self):
        selected_entry = self.listbox.get(tk.ACTIVE)
        if selected_entry:
            category = self.category_var.get()
            self.knowledge_manager.delete_entry(selected_entry, category)
            self.load_entries()
        else:
            messagebox.showwarning("Selection Error", "No entry selected.")

    def search_entries(self, event):
        query = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        category = self.category_var.get()
        entries = self.knowledge_manager.load_entries(category)
        for entry in entries:
            if query in entry.lower():
                self.listbox.insert(tk.END, entry)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()