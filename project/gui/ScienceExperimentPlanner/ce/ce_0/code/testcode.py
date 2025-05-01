import unittest
import os
from experiment import Experiment
from file_management import save_to_file, load_from_file

class TestExperimentPlanner(unittest.TestCase):

    def setUp(self):
        self.experiment_title = "Sample Experiment"
        self.experiment_objectives = "To demonstrate the reaction between vinegar and baking soda"
        self.experiment_materials = "Vinegar, Baking Soda, Container, Spoon"
        self.experiment_procedures = "Mix vinegar and baking soda in the container, Observe the reaction"
        self.experiment = Experiment(self.experiment_title, self.experiment_objectives, self.experiment_materials, self.experiment_procedures)

    def test_create_experiment(self):
        # Functionality 1: Input and Organize Experiment Details
        self.assertEqual(self.experiment.title, self.experiment_title)
        self.assertEqual(self.experiment.objectives, self.experiment_objectives)
        self.assertEqual(self.experiment.materials, self.experiment_materials)
        self.assertEqual(self.experiment.procedures, self.experiment_procedures)

        # Simulate saving the experiment
        experiment_data = {
            'title': self.experiment.title,
            'objectives': self.experiment.objectives,
            'materials': self.experiment.materials,
            'procedures': self.experiment.procedures
        }
        save_to_file(experiment_data, f'experiments/{self.experiment.title}.txt')

        # Check if the experiment is saved correctly
        loaded_data = load_from_file(f'experiments/{self.experiment.title}.txt')
        self.assertEqual(loaded_data['title'], self.experiment_title)
        self.assertEqual(loaded_data['objectives'], self.experiment_objectives)
        self.assertEqual(loaded_data['materials'], self.experiment_materials)
        self.assertEqual(loaded_data['procedures'], self.experiment_procedures)

    def test_record_observation(self):
        # Functionality 3: Record Observations and Results
        observation = "Initial reaction observed with bubbling and fizzing"
        self.experiment.record_observation(observation)

        # Check if the observation is recorded
        with open(f'observations/{self.experiment.title}_observations.txt', 'r') as obs_file:
            recorded_observations = obs_file.readlines()
            self.assertIn(observation + '\n', recorded_observations)

    def test_load_experiment(self):
        # Functionality 1: Load existing experiments
        if not os.path.exists('experiments'):
            os.makedirs('experiments')
        experiment_data = {
            'title': self.experiment.title,
            'objectives': self.experiment.objectives,
            'materials': self.experiment.materials,
            'procedures': self.experiment.procedures
        }
        save_to_file(experiment_data, f'experiments/{self.experiment.title}.txt')

        loaded_data = load_from_file(f'experiments/{self.experiment.title}.txt')
        self.assertEqual(loaded_data['title'], self.experiment_title)

    def test_delete_experiment(self):
        # Functionality 1: Delete an experiment
        experiment_file_path = f'experiments/{self.experiment.title}.txt'
        if os.path.exists(experiment_file_path):
            os.remove(experiment_file_path)
        self.assertFalse(os.path.exists(experiment_file_path))

    def test_edit_experiment(self):
        # Functionality 1: Edit an experiment
        new_objectives = "To explore the reaction between vinegar and baking soda"
        self.experiment.objectives = new_objectives
        self.assertEqual(self.experiment.objectives, new_objectives)

        # Simulate saving the edited experiment
        experiment_data = {
            'title': self.experiment.title,
            'objectives': self.experiment.objectives,
            'materials': self.experiment.materials,
            'procedures': self.experiment.procedures
        }
        save_to_file(experiment_data, f'experiments/{self.experiment.title}.txt')

        # Check if the edited experiment is saved correctly
        loaded_data = load_from_file(f'experiments/{self.experiment.title}.txt')
        self.assertEqual(loaded_data['objectives'], new_objectives)

if __name__ == '__main__':
    unittest.main()
