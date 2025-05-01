import tkinter as tk
from tkinter import messagebox
from experiments import ExperimentManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Experiment Planner")
        self.experiment_manager = ExperimentManager()
        self.experiment_manager.load_experiments()
        self.create_widgets()

    def create_widgets(self):
        self.experiment_listbox = tk.Listbox(self.root)
        self.experiment_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.root, text="Add Experiment", command=self.add_experiment)
        self.add_button.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self.root, text="Edit Experiment", command=self.edit_experiment)
        self.edit_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.root, text="Delete Experiment", command=self.delete_experiment)
        self.delete_button.pack(side=tk.LEFT)

        self.update_experiment_list()

    def update_experiment_list(self):
        self.experiment_listbox.delete(0, tk.END)
        for experiment in self.experiment_manager.experiments:
            self.experiment_listbox.insert(tk.END, experiment.title)

    def add_experiment(self):
        # Implementation for adding an experiment
        pass

    def edit_experiment(self):
        # Implementation for editing an experiment
        pass

    def delete_experiment(self):
        selected_index = self.experiment_listbox.curselection()
        if selected_index:
            experiment_id = selected_index[0]
            self.experiment_manager.delete_experiment(experiment_id)
            self.update_experiment_list()
        else:
            messagebox.showwarning("Warning", "Select an experiment to delete.")

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()