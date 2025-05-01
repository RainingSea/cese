import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Main:
    def __init__(self):
        self.knowledge_manager = KnowledgeManager()

    def main(self):
        self.root = tk.Tk()
        self.root.title("Knowledge Tracker")

        self.type_var = tk.StringVar()
        self.content_var = tk.StringVar()

        tk.Label(self.root, text="Type:").grid(row=0, column=0)
        tk.OptionMenu(self.root, self.type_var, "theory", "concept", "experiment").grid(row=0, column=1)

        tk.Label(self.root, text="Content:").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.content_var).grid(row=1, column=1)

        tk.Button(self.root, text="Add Knowledge", command=self.add_knowledge).grid(row=2, column=0)
        tk.Button(self.root, text="Update Knowledge", command=self.update_knowledge).grid(row=2, column=1)
        tk.Button(self.root, text="Retrieve Knowledge", command=self.retrieve_knowledge).grid(row=3, column=0, columnspan=2)

        self.display_area = tk.Text(self.root, height=10, width=50)
        self.display_area.grid(row=4, column=0, columnspan=2)

        self.root.mainloop()

    def add_knowledge(self):
        knowledge_type = self.type_var.get()
        content = self.content_var.get()
        if knowledge_type and content:
            self.knowledge_manager.add_knowledge(knowledge_type, content)
            messagebox.showinfo("Success", "Knowledge added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please select a type and enter content.")

    def update_knowledge(self):
        knowledge_type = self.type_var.get()
        old_content = simpledialog.askstring("Update Knowledge", "Enter the old content:")
        new_content = self.content_var.get()
        if knowledge_type and old_content and new_content:
            self.knowledge_manager.update_knowledge(knowledge_type, old_content, new_content)
            messagebox.showinfo("Success", "Knowledge updated successfully!")
        else:
            messagebox.showwarning("Input Error", "Please provide all required fields.")

    def retrieve_knowledge(self):
        knowledge_type = self.type_var.get()
        if knowledge_type:
            knowledge_list = self.knowledge_manager.retrieve_knowledge(knowledge_type)
            self.display_area.delete(1.0, tk.END)
            self.display_area.insert(tk.END, "\n".join(knowledge_list))
        else:
            messagebox.showwarning("Input Error", "Please select a type.")

class KnowledgeManager:
    def __init__(self):
        self.file_paths = {
            "theory": "theories.txt",
            "concept": "concepts.txt",
            "experiment": "experiments.txt"
        }

    def add_knowledge(self, type: str, content: str):
        with open(self.file_paths[type], 'a') as file:
            file.write(content + "\n")

    def update_knowledge(self, type: str, old_content: str, new_content: str):
        with open(self.file_paths[type], 'r') as file:
            lines = file.readlines()
        with open(self.file_paths[type], 'w') as file:
            for line in lines:
                if line.strip() == old_content:
                    file.write(new_content + "\n")
                else:
                    file.write(line)

    def retrieve_knowledge(self, type: str):
        with open(self.file_paths[type], 'r') as file:
            return [line.strip() for line in file.readlines()]

if __name__ == "__main__":
    app = Main()
    app.main()