import os
from experiment import Experiment

class ExperimentManager:
    def __init__(self):
        self.experiments = []

    def add_experiment(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        experiment = Experiment(title, objectives, materials, procedures)
        self.experiments.append(experiment)
        self.save_experiment(experiment)

    def save_experiment(self, experiment: Experiment) -> None:
        filename = f"{experiment.title}.txt"
        with open(filename, 'w') as file:
            file.write(experiment.to_string())

    def load_experiments(self) -> list:
        experiments = []
        for filename in os.listdir('.'):
            if filename.endswith('.txt'):
                with open(filename, 'r') as file:
                    content = file.read()
                    title = filename[:-4]  # Remove .txt
                    # Assuming the content is structured correctly
                    experiments.append(content)
        return experiments