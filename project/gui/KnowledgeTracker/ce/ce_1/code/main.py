import tkinter as tk
from tkinter import messagebox, StringVar, Listbox, END
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()
        self.root = tk.Tk()
        self.root.title("Knowledge Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.knowledge_input = tk.Entry(self.root, width=50)
        self.knowledge_input.pack(pady=10)

        self.category_var = StringVar(self.root)
        self.category_var.set("theories")  # default value
        self.category_menu = tk.OptionMenu(self.root, self.category_var, "theories", "concepts", "experiments")
        self.category_menu.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_knowledge)
        self.submit_button.pack(pady=10)

        self.knowledge_listbox = Listbox(self.root, width=50, height=10)
        self.knowledge_listbox.pack(pady=10)
        self.refresh_list()

        self.update_button = tk.Button(self.root, text="Update", command=self.update_knowledge)
        self.update_button.pack(pady=10)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.refresh_button.pack(pady=10)

    def submit_knowledge(self):
        knowledge = self.knowledge_input.get()
        category = self.category_var.get()
        if knowledge:
            self.knowledge_manager.add_knowledge(category, knowledge)
            self.knowledge_input.delete(0, END)
            self.refresh_list()
        else:
            messagebox.showwarning("Input Error", "Please enter some knowledge.")

    def update_knowledge(self):
        selected = self.knowledge_listbox.curselection()
        if selected:
            old_knowledge = self.knowledge_listbox.get(selected)
            new_knowledge = self.knowledge_input.get()
            category = self.category_var.get()
            if new_knowledge:
                self.knowledge_manager.update_knowledge(category, old_knowledge, new_knowledge)
                self.knowledge_input.delete(0, END)
                self.refresh_list()
            else:
                messagebox.showwarning("Input Error", "Please enter new knowledge.")
        else:
            messagebox.showwarning("Selection Error", "Please select an entry to update.")

    def refresh_list(self):
        self.knowledge_listbox.delete(0, END)
        category = self.category_var.get()
        knowledge_list = self.knowledge_manager.retrieve_knowledge(category)
        for knowledge in knowledge_list:
            self.knowledge_listbox.insert(END, knowledge)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()