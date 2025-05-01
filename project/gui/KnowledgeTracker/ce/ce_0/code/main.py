from tkinter import Tk, Menu, Listbox, Entry, Button, StringVar, END, OptionMenu
from knowledge_tracker import KnowledgeTracker

class Main:
    def __init__(self):
        self.knowledge_tracker = KnowledgeTracker()
        self.root = Tk()
        self.root.title("Knowledge Tracker")
        self._create_widgets()
        self.root.mainloop()

    def _create_widgets(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.listbox = Listbox(self.root)
        self.listbox.pack()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.category_var = StringVar(self.root)
        self.category_var.set("Select Category")
        self.category_menu = OptionMenu(self.root, self.category_var, "Theory", "Concept", "Experiment")
        self.category_menu.pack()

        self.add_button = Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.pack()

        self.update_button = Button(self.root, text="Update Entry", command=self.update_entry)
        self.update_button.pack()

        self.load_entries()

    def load_entries(self):
        self.listbox.delete(0, END)
        for theory in self.knowledge_tracker.retrieve_theories():
            self.listbox.insert(END, f"Theory: {theory}")
        for concept in self.knowledge_tracker.retrieve_concepts():
            self.listbox.insert(END, f"Concept: {concept}")
        for experiment in self.knowledge_tracker.retrieve_experiments():
            self.listbox.insert(END, f"Experiment: {experiment}")

    def add_entry(self):
        entry = self.entry.get()
        category = self.category_var.get()
        if category == "Theory":
            self.knowledge_tracker.add_theory(entry)
        elif category == "Concept":
            self.knowledge_tracker.add_concept(entry)
        elif category == "Experiment":
            self.knowledge_tracker.add_experiment(entry)
        self.load_entries()

    def update_entry(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            entry = self.entry.get()
            category = self.category_var.get()
            index = selected_index[0]
            if category == "Theory":
                self.knowledge_tracker.update_theory(index, entry)
            elif category == "Concept":
                self.knowledge_tracker.update_concept(index, entry)
            elif category == "Experiment":
                self.knowledge_tracker.update_experiment(index, entry)
            self.load_entries()

if __name__ == "__main__":
    Main()