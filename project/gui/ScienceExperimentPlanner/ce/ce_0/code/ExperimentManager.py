import json
from Experiment import Experiment
from Observation import Observation

class ExperimentManager:
    def __init__(self):
        self.experiments = []
        self.load_experiments()

    def add_experiment(self, details: dict):
        new_id = len(self.experiments) + 1
        experiment = Experiment(new_id, details['objectives'], details['materials'], details['procedure'])
        self.experiments.append(experiment)
        self.save_experiments()

    def update_experiment(self, id: int, details: dict):
        for experiment in self.experiments:
            if experiment.id == id:
                experiment.objectives = details['objectives']
                experiment.materials = details['materials']
                experiment.procedure = details['procedure']
                self.save_experiments()
                break

    def get_experiments(self):
        return [vars(experiment) for experiment in self.experiments]

    def load_experiments(self):
        try:
            with open('experiments.txt', 'r') as file:
                data = file.readlines()
                for line in data:
                    experiment_data = json.loads(line.strip())
                    experiment = Experiment(experiment_data['id'], experiment_data['objectives'],
                                            experiment_data['materials'], experiment_data['procedure'])
                    experiment.status = experiment_data['status']
                    self.experiments.append(experiment)
        except FileNotFoundError:
            pass

    def save_experiments(self):
        with open('experiments.txt', 'w') as file:
            for experiment in self.experiments:
                file.write(json.dumps(vars(experiment)) + '\n')