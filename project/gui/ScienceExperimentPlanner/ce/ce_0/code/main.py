import tkinter as tk
from tkinter import messagebox
from ExperimentManager import ExperimentManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Tracker")
        self.experiment_manager = ExperimentManager()

        self.create_widgets()

    def create_widgets(self):
        self.objectives_label = tk.Label(self.root, text="Objectives:")
        self.objectives_label.pack()
        self.objectives_entry = tk.Entry(self.root)
        self.objectives_entry.pack()

        self.materials_label = tk.Label(self.root, text="Materials:")
        self.materials_label.pack()
        self.materials_entry = tk.Entry(self.root)
        self.materials_entry.pack()

        self.procedure_label = tk.Label(self.root, text="Procedure:")
        self.procedure_label.pack()
        self.procedure_entry = tk.Entry(self.root)
        self.procedure_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Experiment", command=self.add_experiment)
        self.add_button.pack()

        self.experiment_list = tk.Listbox(self.root)
        self.experiment_list.pack(fill=tk.BOTH, expand=True)

        self.load_experiments()

    def add_experiment(self):
        objectives = self.objectives_entry.get()
        materials = self.materials_entry.get()
        procedure = self.procedure_entry.get()

        if not objectives or not materials or not procedure:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        details = {'objectives': objectives, 'materials': materials, 'procedure': procedure}
        self.experiment_manager.add_experiment(details)
        self.load_experiments()

    def load_experiments(self):
        self.experiment_list.delete(0, tk.END)
        experiments = self.experiment_manager.get_experiments()
        for experiment in experiments:
            self.experiment_list.insert(tk.END, f"ID: {experiment['id']}, Objectives: {experiment['objectives']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()