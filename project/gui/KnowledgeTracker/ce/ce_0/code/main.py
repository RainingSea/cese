import tkinter as tk
from tkinter import messagebox, ttk
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager('knowledge.json')
        self.root = tk.Tk()
        self.root.title("Knowledge Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.input_field = tk.Entry(self.root, width=50)
        self.input_field.pack(pady=10)

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_dropdown['values'] = ('Physics', 'Chemistry', 'Biology')
        self.category_dropdown.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Knowledge", command=self.add_knowledge)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Knowledge", command=self.update_knowledge)
        self.update_button.pack(pady=5)

        self.retrieve_button = tk.Button(self.root, text="Retrieve Knowledge", command=self.retrieve_knowledge)
        self.retrieve_button.pack(pady=5)

        self.text_area = tk.Text(self.root, height=15, width=70)
        self.text_area.pack(pady=10)

    def add_knowledge(self):
        entry = {
            'id': len(self.knowledge_manager.retrieve_knowledge()) + 1,
            'content': self.input_field.get(),
            'category': self.category_var.get()
        }
        self.knowledge_manager.add_knowledge(entry)
        messagebox.showinfo("Info", "Knowledge added successfully!")
        self.input_field.delete(0, tk.END)

    def update_knowledge(self):
        entry = {
            'id': int(self.input_field.get().split()[0]),  # Assuming the first word is the ID
            'content': " ".join(self.input_field.get().split()[1:]),
            'category': self.category_var.get()
        }
        self.knowledge_manager.update_knowledge(entry)
        messagebox.showinfo("Info", "Knowledge updated successfully!")
        self.input_field.delete(0, tk.END)

    def retrieve_knowledge(self):
        knowledge_list = self.knowledge_manager.retrieve_knowledge()
        self.text_area.delete(1.0, tk.END)
        for entry in knowledge_list:
            self.text_area.insert(tk.END, f"ID: {entry['id']}, Content: {entry['content']}, Category: {entry['category']}\n")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()