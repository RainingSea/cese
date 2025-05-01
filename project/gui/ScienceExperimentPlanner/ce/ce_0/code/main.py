import os
from experiment import Experiment
from file_management import save_to_file, load_from_file

class Main:
    def __init__(self):
        self.experiments = []
        self.load_experiments()

    def main(self) -> None:
        # Entry point of the application
        print("Welcome to the Science Experiment Planner")

    def create_experiment(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        new_experiment = Experiment(title, objectives, materials, procedures)
        self.experiments.append(new_experiment)
        self.save_experiment(new_experiment)

    def edit_experiment(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        for experiment in self.experiments:
            if experiment.title == title:
                experiment.objectives = objectives
                experiment.materials = materials
                experiment.procedures = procedures
                self.save_experiment(experiment)

    def delete_experiment(self, title: str) -> None:
        self.experiments = [exp for exp in self.experiments if exp.title != title]
        os.remove(f'experiments/{title}.txt')

    def load_experiments(self) -> None:
        if not os.path.exists('experiments'):
            os.makedirs('experiments')
        for filename in os.listdir('experiments'):
            if filename.endswith('.txt'):
                experiment_data = load_from_file(f'experiments/{filename}')
                experiment = Experiment(
                    title=experiment_data['title'],
                    objectives=experiment_data['objectives'],
                    materials=experiment_data['materials'],
                    procedures=experiment_data['procedures']
                )
                self.experiments.append(experiment)

    def save_experiment(self, experiment: Experiment) -> None:
        experiment_data = {
            'title': experiment.title,
            'objectives': experiment.objectives,
            'materials': experiment.materials,
            'procedures': experiment.procedures
        }
        save_to_file(experiment_data, f'experiments/{experiment.title}.txt')