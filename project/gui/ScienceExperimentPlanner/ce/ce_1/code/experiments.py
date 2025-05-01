import os

class Experiment:
    def __init__(self, title, objectives, materials, procedures, status="Not Started"):
        self.title = title
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.status = status
        self.observations = []

    def record_observation(self, observation):
        self.observations.append(observation)

    def update_status(self, status):
        self.status = status

class ExperimentManager:
    def __init__(self):
        self.experiments = []

    def add_experiment(self, experiment):
        self.experiments.append(experiment)
        self.save_experiments()

    def edit_experiment(self, experiment_id, updated_experiment):
        if 0 <= experiment_id < len(self.experiments):
            self.experiments[experiment_id] = updated_experiment
            self.save_experiments()

    def delete_experiment(self, experiment_id):
        if 0 <= experiment_id < len(self.experiments):
            del self.experiments[experiment_id]
            self.save_experiments()

    def load_experiments(self):
        if os.path.exists("experiments.txt"):
            with open("experiments.txt", "r") as file:
                for line in file:
                    title, objectives, materials, procedures, status = line.strip().split("|")
                    materials_list = materials.split(",")
                    experiment = Experiment(title, objectives, materials_list, procedures, status)
                    self.experiments.append(experiment)

    def save_experiments(self):
        with open("experiments.txt", "w") as file:
            for experiment in self.experiments:
                materials_str = ",".join(experiment.materials)
                file.write(f"{experiment.title}|{experiment.objectives}|{materials_str}|{experiment.procedures}|{experiment.status}\n")