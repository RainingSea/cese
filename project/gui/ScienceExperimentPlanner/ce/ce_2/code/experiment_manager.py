import os

class ExperimentManager:
    def __init__(self):
        self.experiments = []

    def add_experiment(self, experiment: 'Experiment'):
        self.experiments.append(experiment)

    def get_experiments(self) -> list:
        return self.experiments

    def save_experiments(self):
        with open('experiments.txt', 'w') as file:
            for experiment in self.experiments:
                file.write(experiment.to_string() + '\n')

    def load_experiments(self):
        if os.path.exists('experiments.txt'):
            with open('experiments.txt', 'r') as file:
                for line in file:
                    data = line.strip().split('|')
                    if len(data) == 4:
                        objective, materials, procedure, status = data
                        experiment = Experiment(objective, materials, procedure)
                        experiment.update_status(status)
                        self.add_experiment(experiment)