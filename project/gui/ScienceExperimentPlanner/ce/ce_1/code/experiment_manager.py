import json
import os
from experiment import Experiment

class ExperimentManager:
    def __init__(self) -> None:
        self.experiments = []

    def add_experiment(self, experiment: Experiment) -> None:
        self.experiments.append(experiment)

    def load_experiment(self, title: str) -> Experiment:
        file_path = f'experiments/{title}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                return Experiment.from_dict(data)
        raise FileNotFoundError(f'Experiment titled "{title}" not found.')

    def save_experiment(self, experiment: Experiment) -> None:
        file_path = f'experiments/{experiment.title}.json'
        with open(file_path, 'w') as file:
            json.dump(experiment.to_dict(), file, indent=4)