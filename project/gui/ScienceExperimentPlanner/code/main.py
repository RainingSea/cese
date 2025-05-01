import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class Experiment:
    def __init__(self, title: str, objectives: str, materials: str, procedures: str, status: str = "Not Started") -> None:
        self.title = title
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.status = status
        self.observations = self.load_observations()

    def add_observation(self, observation: str) -> None:
        if observation:
            self.observations.append(observation)
            self.record_observation(observation)
        else:
            raise ValueError("Observation cannot be empty.")

    def record_observation(self, observation: str) -> None:
        with open(f'observations/{self.title.replace(" ", "_")}_observations.txt', 'a') as obs_file:
            obs_file.write(observation + '\n')

    def load_observations(self) -> list:
        observations_file = f'observations/{self.title.replace(" ", "_")}_observations.txt'
        if os.path.exists(observations_file):
            with open(observations_file, 'r') as obs_file:
                return obs_file.read().splitlines()
        return []

    def update_status(self, new_status: str) -> None:
        self.status = new_status

    def track_progress(self, status: str) -> None:
        self.update_status(status)
        self.save_progress()

    def save_progress(self) -> None:
        with open("progress.txt", "w") as prog_file:
            for experiment in ExperimentManager().experiments:
                prog_file.write(f"{experiment.title}|{experiment.status}\n")

    def get_details(self) -> str:
        return (f"Title: {self.title}\nObjectives: {self.objectives}\n"
                f"Materials: {self.materials}\nProcedures: {self.procedures}\n"
                f"Status: {self.status}\nObservations: {', '.join(self.observations)}")

class ExperimentManager:
    def __init__(self) -> None:
        self.experiments = []
        self.load_experiments()

    def create_experiment(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        experiment = Experiment(title, objectives, materials, procedures)
        self.experiments.append(experiment)
        self.save_experiments()

    def edit_experiment(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        for experiment in self.experiments:
            if experiment.title == title:
                experiment.objectives = objectives
                experiment.materials = materials
                experiment.procedures = procedures
                self.save_experiment(experiment)
                return
        raise ValueError("Experiment not found.")

    def delete_experiment(self, title: str) -> None:
        self.experiments = [exp for exp in self.experiments if exp.title != title]
        self.save_experiments()
        os.remove(f'experiments/{title.replace(" ", "_")}.txt')
        os.remove(f'observations/{title.replace(" ", "_")}_observations.txt')

    def load_experiments(self) -> None:
        if not os.path.exists('experiments'):
            os.makedirs('experiments')
        if not os.path.exists('observations'):
            os.makedirs('observations')
        if os.path.exists('experiment_index.txt'):
            with open('experiment_index.txt', 'r') as index_file:
                titles = index_file.read().splitlines()
                for title in titles:
                    self.load_experiment(title)

    def load_experiment(self, title: str) -> None:
        filename = f'experiments/{title.replace(" ", "_")}.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                objectives, materials, procedures, status = file.read().splitlines()
                experiment = Experiment(title, objectives, materials, procedures)
                experiment.status = status
                self.experiments.append(experiment)

    def save_experiments(self) -> None:
        with open('experiment_index.txt', 'w') as index_file:
            for experiment in self.experiments:
                index_file.write(experiment.title + '\n')
                self.save_experiment(experiment)

    def save_experiment(self, experiment: Experiment) -> None:
        filename = f'experiments/{experiment.title.replace(" ", "_")}.txt'
        with open(filename, 'w') as file:
            file.write(f"{experiment.objectives}\n{experiment.materials}\n{experiment.procedures}\n{experiment.status}")

    def search_experiment(self, keyword: str) -> list:
        return [exp for exp in self.experiments if keyword.lower() in exp.title.lower()]

class Main:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.experiment_manager = ExperimentManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.master.title("Science Experiment Planner")
        self.experiment_listbox = tk.Listbox(self.master)
        self.experiment_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_experiment_list()

        tk.Button(self.master, text="Create Experiment", command=self.create_experiment).pack()
        tk.Button(self.master, text="Edit Experiment", command=self.edit_experiment).pack()
        tk.Button(self.master, text="Delete Experiment", command=self.delete_experiment).pack()
        tk.Button(self.master, text="Search Experiment", command=self.search_experiment).pack()

    def load_experiment_list(self) -> None:
        self.experiment_listbox.delete(0, tk.END)
        for experiment in self.experiment_manager.experiments:
            self.experiment_listbox.insert(tk.END, experiment.title)

    def create_experiment(self) -> None:
        title = simpledialog.askstring("Input", "Enter experiment title:")
        objectives = simpledialog.askstring("Input", "Enter objectives:")
        materials = simpledialog.askstring("Input", "Enter materials:")
        procedures = simpledialog.askstring("Input", "Enter procedures:")
        if title and objectives and materials and procedures:
            self.experiment_manager.create_experiment(title, objectives, materials, procedures)
            self.load_experiment_list()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def edit_experiment(self) -> None:
        selected = self.experiment_listbox.curselection()
        if selected:
            title = self.experiment_listbox.get(selected)
            objectives = simpledialog.askstring("Input", "Enter new objectives:")
            materials = simpledialog.askstring("Input", "Enter new materials:")
            procedures = simpledialog.askstring("Input", "Enter new procedures:")
            if objectives and materials and procedures:
                self.experiment_manager.edit_experiment(title, objectives, materials, procedures)
                self.load_experiment_list()
            else:
                messagebox.showerror("Error", "All fields must be filled.")
        else:
            messagebox.showerror("Error", "No experiment selected.")

    def delete_experiment(self) -> None:
        selected = self.experiment_listbox.curselection()
        if selected:
            title = self.experiment_listbox.get(selected)
            self.experiment_manager.delete_experiment(title)
            self.load_experiment_list()
        else:
            messagebox.showerror("Error", "No experiment selected.")

    def search_experiment(self) -> None:
        keyword = simpledialog.askstring("Input", "Enter search keyword:")
        if keyword:
            results = self.experiment_manager.search_experiment(keyword)
            self.experiment_listbox.delete(0, tk.END)
            for experiment in results:
                self.experiment_listbox.insert(tk.END, experiment.title)
        else:
            messagebox.showerror("Error", "Search keyword cannot be empty.")

def main() -> None:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()