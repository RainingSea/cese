import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Experiment:
    def __init__(self, objectives, materials, procedures, status="Not Started"):
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.status = status

    def record_observation(self, observation):
        with open("observations.txt", "a") as obs_file:
            obs_file.write(f"{self.objectives}|{observation}\n")

    def get_details(self):
        return f"Objectives: {self.objectives}\nMaterials: {', '.join(self.materials)}\nProcedures: {self.procedures}\nStatus: {self.status}"

class ExperimentManager:
    def __init__(self):
        self.experiments = []

    def add_experiment(self, details):
        objectives, materials, procedures = details.split('|')
        materials_list = materials.split(',')
        new_experiment = Experiment(objectives, materials_list, procedures)
        self.experiments.append(new_experiment)
        self.save_experiments()

    def edit_experiment(self, id, details):
        objectives, materials, procedures = details.split('|')
        materials_list = materials.split(',')
        self.experiments[id].objectives = objectives
        self.experiments[id].materials = materials_list
        self.experiments[id].procedures = procedures
        self.save_experiments()

    def delete_experiment(self, id):
        del self.experiments[id]
        self.save_experiments()

    def track_progress(self, id, status):
        self.experiments[id].status = status
        self.save_progress()

    def save_experiments(self):
        with open("experiments.txt", "w") as exp_file:
            for experiment in self.experiments:
                materials = ','.join(experiment.materials)
                exp_file.write(f"{experiment.objectives}|{materials}|{experiment.procedures}|{experiment.status}\n")

    def save_progress(self):
        with open("progress.txt", "w") as prog_file:
            for experiment in self.experiments:
                prog_file.write(f"{experiment.objectives}|{experiment.status}\n")

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Science Experiment Planner")
        self.experiment_manager = ExperimentManager()
        self.load_experiments()
        self.create_ui()

    def create_ui(self):
        self.experiment_listbox = tk.Listbox(self.master)
        self.experiment_listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.master, text="Add Experiment", command=self.add_experiment)
        self.add_button.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self.master, text="Edit Experiment", command=self.edit_experiment)
        self.edit_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.master, text="Delete Experiment", command=self.delete_experiment)
        self.delete_button.pack(side=tk.LEFT)

        self.progress_button = tk.Button(self.master, text="Mark as Completed", command=self.mark_completed)
        self.progress_button.pack(side=tk.LEFT)

        self.update_experiment_list()

    def add_experiment(self):
        details = simpledialog.askstring("Input", "Enter objectives|materials (comma separated)|procedures:")
        if details:
            self.experiment_manager.add_experiment(details)
            self.update_experiment_list()

    def edit_experiment(self):
        selected = self.experiment_listbox.curselection()
        if selected:
            index = selected[0]
            details = simpledialog.askstring("Input", "Enter new objectives|materials (comma separated)|procedures:")
            if details:
                self.experiment_manager.edit_experiment(index, details)
                self.update_experiment_list()

    def delete_experiment(self):
        selected = self.experiment_listbox.curselection()
        if selected:
            index = selected[0]
            self.experiment_manager.delete_experiment(index)
            self.update_experiment_list()

    def mark_completed(self):
        selected = self.experiment_listbox.curselection()
        if selected:
            index = selected[0]
            self.experiment_manager.track_progress(index, "Completed")
            self.update_experiment_list()

    def update_experiment_list(self):
        self.experiment_listbox.delete(0, tk.END)
        for experiment in self.experiment_manager.experiments:
            self.experiment_listbox.insert(tk.END, experiment.objectives)

    def load_experiments(self):
        try:
            with open("experiments.txt", "r") as exp_file:
                for line in exp_file:
                    objectives, materials, procedures, status = line.strip().split('|')
                    materials_list = materials.split(',')
                    experiment = Experiment(objectives, materials_list, procedures, status)
                    self.experiment_manager.experiments.append(experiment)
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()