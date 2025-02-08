import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os

class Experiment:
    def __init__(self, id, objective, materials, procedure, expected_results, status="Pending"):
        self.id = id
        self.objective = objective
        self.materials = materials
        self.procedure = procedure
        self.expected_results = expected_results
        self.status = status

    def record_observation(self, observation):
        observation_manager.record_observation(self.id, observation)

    def to_string(self):
        return f"{self.id},{self.objective},{self.materials},{self.procedure},{self.expected_results},{self.status}"

class ExperimentManager:
    def __init__(self):
        self.experiments = []
        self.load_experiments()

    def add_experiment(self, objective, materials, procedure, expected_results):
        experiment_id = len(self.experiments) + 1
        new_experiment = Experiment(experiment_id, objective, materials, procedure, expected_results)
        self.experiments.append(new_experiment)
        self.save_experiments()

    def load_experiments(self):
        if os.path.exists('experiments.txt'):
            with open('experiments.txt', 'r') as file:
                for line in file:
                    id, objective, materials, procedure, expected_results, status = line.strip().split(',')
                    experiment = Experiment(int(id), objective, materials, procedure, expected_results, status)
                    self.experiments.append(experiment)

    def save_experiments(self):
        with open('experiments.txt', 'w') as file:
            for experiment in self.experiments:
                file.write(experiment.to_string() + '\n')

    def get_experiments(self):
        return self.experiments

class Observation:
    def __init__(self, experiment_id, observation, timestamp):
        self.experiment_id = experiment_id
        self.observation = observation
        self.timestamp = timestamp

    def to_string(self):
        return f"{self.experiment_id},{self.observation},{self.timestamp}"

class ObservationManager:
    def __init__(self):
        self.observations = []
        self.load_observations()

    def record_observation(self, experiment_id, observation):
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        new_observation = Observation(experiment_id, observation, timestamp)
        self.observations.append(new_observation)
        self.save_observations()

    def load_observations(self):
        if os.path.exists('observations.txt'):
            with open('observations.txt', 'r') as file:
                for line in file:
                    experiment_id, observation, timestamp = line.strip().split(',')
                    obs = Observation(int(experiment_id), observation, timestamp)
                    self.observations.append(obs)

    def save_observations(self):
        with open('observations.txt', 'w') as file:
            for observation in self.observations:
                file.write(observation.to_string() + '\n')

def add_experiment():
    objective = simpledialog.askstring("Input", "Enter experiment objective:")
    materials = simpledialog.askstring("Input", "Enter materials:")
    procedure = simpledialog.askstring("Input", "Enter procedure:")
    expected_results = simpledialog.askstring("Input", "Enter expected results:")
    experiment_manager.add_experiment(objective, materials, procedure, expected_results)
    messagebox.showinfo("Success", "Experiment added successfully!")

def view_experiments():
    experiments = experiment_manager.get_experiments()
    display_text = "\n".join([exp.to_string() for exp in experiments])
    messagebox.showinfo("Experiments", display_text)

def record_observation():
    experiment_id = simpledialog.askinteger("Input", "Enter experiment ID:")
    observation = simpledialog.askstring("Input", "Enter observation:")
    experiment = next((exp for exp in experiment_manager.get_experiments() if exp.id == experiment_id), None)
    if experiment:
        experiment.record_observation(observation)
        messagebox.showinfo("Success", "Observation recorded successfully!")
    else:
        messagebox.showerror("Error", "Experiment ID not found.")

experiment_manager = ExperimentManager()
observation_manager = ObservationManager()

root = tk.Tk()
root.title("Science Experiment Planner")

add_button = tk.Button(root, text="Add Experiment", command=add_experiment)
add_button.pack()

view_button = tk.Button(root, text="View Experiments", command=view_experiments)
view_button.pack()

record_button = tk.Button(root, text="Record Observations", command=record_observation)
record_button.pack()

root.mainloop()