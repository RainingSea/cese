import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox
from knowledge_manager import KnowledgeManager

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager('knowledge.json')
        self.root = tk.Tk()
        self.root.title("Scientific Knowledge Manager")

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.content_entry = tk.Text(self.root, height=10, width=50)
        self.content_entry.pack()

        self.save_button = tk.Button(self.root, text="Save Knowledge", command=self.save_knowledge)
        self.save_button.pack()

        self.knowledge_listbox = Listbox(self.root)
        self.knowledge_listbox.pack()
        self.knowledge_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack()

        self.load_knowledge()

    def save_knowledge(self):
        title = self.title_entry.get()
        category = self.category_entry.get()
        content = self.content_entry.get("1.0", tk.END).strip()

        if title and category and content:
            knowledge = {
                "title": title,
                "category": category,
                "content": content
            }
            self.knowledge_manager.save_knowledge(knowledge)
            self.load_knowledge()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def load_knowledge(self):
        self.knowledge_listbox.delete(0, tk.END)
        for knowledge in self.knowledge_manager.knowledge_list:
            self.knowledge_listbox.insert(tk.END, knowledge.title)

    def on_select(self, event):
        selected_index = self.knowledge_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            knowledge = self.knowledge_manager.knowledge_list[index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, knowledge.title)
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, knowledge.category)
            self.content_entry.delete("1.0", tk.END)
            self.content_entry.insert("1.0", knowledge.content)

    def delete_selected(self):
        selected_index = self.knowledge_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.knowledge_manager.delete_knowledge(index)
            self.load_knowledge()
            self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.content_entry.delete("1.0", tk.END)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()