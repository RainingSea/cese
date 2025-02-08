import tkinter as tk
from tkinter import messagebox
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()
        self.root = tk.Tk()
        self.root.title("Knowledge Tracker")
        
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.pack()
        
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()
        
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        
        self.content_label = tk.Label(self.root, text="Content:")
        self.content_label.pack()
        
        self.content_entry = tk.Entry(self.root)
        self.content_entry.pack()
        
        self.add_button = tk.Button(self.root, text="Add Knowledge", command=self.add_knowledge)
        self.add_button.pack()
        
        self.update_button = tk.Button(self.root, text="Update Knowledge", command=self.update_knowledge)
        self.update_button.pack()
        
        self.retrieve_button = tk.Button(self.root, text="Retrieve Knowledge", command=self.retrieve_knowledge)
        self.retrieve_button.pack()
        
        self.display_area = tk.Text(self.root, height=10, width=50)
        self.display_area.pack()

    def add_knowledge(self):
        category = self.category_entry.get()
        title = self.title_entry.get()
        content = self.content_entry.get()
        
        try:
            self.knowledge_manager.add_knowledge(category, title, content)
            messagebox.showinfo("Success", "Knowledge added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_knowledge(self):
        category = self.category_entry.get()
        title = self.title_entry.get()
        new_content = self.content_entry.get()
        
        try:
            self.knowledge_manager.update_knowledge(category, title, new_content)
            messagebox.showinfo("Success", "Knowledge updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def retrieve_knowledge(self):
        category = self.category_entry.get()
        
        try:
            knowledge_list = self.knowledge_manager.retrieve_knowledge(category)
            self.display_area.delete(1.0, tk.END)
            for entry in knowledge_list:
                self.display_area.insert(tk.END, entry + "\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    Main()