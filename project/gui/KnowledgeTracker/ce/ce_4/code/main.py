import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, StringVar, OptionMenu
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()
        self.root = tk.Tk()
        self.root.title("Scientific Knowledge Manager")

        self.category_var = StringVar(self.root)
        self.category_var.set("Theories")  # Default category

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text="Select Category:").pack()

        categories = list(self.knowledge_manager.knowledge_files.keys())
        OptionMenu(self.root, self.category_var, *categories).pack()

        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack()

        tk.Button(self.root, text="Add Knowledge", command=self.add_knowledge).pack()
        tk.Button(self.root, text="View Knowledge", command=self.view_knowledge).pack()
        tk.Button(self.root, text="Update Knowledge", command=self.update_knowledge).pack()

        self.list_box = Listbox(self.root, height=10, width=50)
        self.list_box.pack()

    def add_knowledge(self):
        knowledge = self.text_area.get("1.0", tk.END).strip()
        category = self.category_var.get()
        if knowledge:
            self.knowledge_manager.add_knowledge(category, knowledge)
            messagebox.showinfo("Success", "Knowledge added successfully!")
            self.text_area.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter some knowledge.")

    def view_knowledge(self):
        category = self.category_var.get()
        knowledge_list = self.knowledge_manager.view_knowledge(category)
        self.list_box.delete(0, tk.END)  # Clear previous list
        for knowledge in knowledge_list:
            self.list_box.insert(tk.END, knowledge.strip())

    def update_knowledge(self):
        category = self.category_var.get()
        old_knowledge = simpledialog.askstring("Input", "Enter the knowledge to update:")
        new_knowledge = simpledialog.askstring("Input", "Enter the new knowledge:")
        if old_knowledge and new_knowledge:
            self.knowledge_manager.update_knowledge(category, old_knowledge, new_knowledge)
            messagebox.showinfo("Success", "Knowledge updated successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter both old and new knowledge.")

if __name__ == "__main__":
    Main()