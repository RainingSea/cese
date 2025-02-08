import tkinter as tk
from tkinter import messagebox, simpledialog
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()
        self.root = tk.Tk()
        self.root.title("Scientific Knowledge Manager")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Add Knowledge", command=self.add_knowledge).pack(pady=10)
        tk.Button(self.root, text="View Knowledge", command=self.view_knowledge).pack(pady=10)
        tk.Button(self.root, text="Update Knowledge", command=self.update_knowledge).pack(pady=10)

    def add_knowledge(self):
        category = simpledialog.askstring("Input", "Enter category (theories, concepts, experiments):")
        knowledge = simpledialog.askstring("Input", "Enter knowledge:")
        if category and knowledge:
            self.knowledge_manager.add_knowledge(category, knowledge)
            messagebox.showinfo("Success", "Knowledge added successfully!")

    def view_knowledge(self):
        category = simpledialog.askstring("Input", "Enter category (theories, concepts, experiments):")
        if category:
            knowledge_list = self.knowledge_manager.view_knowledge(category)
            messagebox.showinfo("Knowledge", "\n".join(knowledge_list))

    def update_knowledge(self):
        category = simpledialog.askstring("Input", "Enter category (theories, concepts, experiments):")
        old_knowledge = simpledialog.askstring("Input", "Enter old knowledge:")
        new_knowledge = simpledialog.askstring("Input", "Enter new knowledge:")
        if category and old_knowledge and new_knowledge:
            self.knowledge_manager.update_knowledge(category, old_knowledge, new_knowledge)
            messagebox.showinfo("Success", "Knowledge updated successfully!")

    def main(self) -> str:
        self.root.mainloop()
        return "Application closed."

if __name__ == "__main__":
    app = Main()
    app.main()