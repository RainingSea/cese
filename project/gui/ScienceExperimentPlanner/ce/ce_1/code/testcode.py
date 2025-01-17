import unittest
import os
import json
from experiment import Experiment
from experiment_manager import ExperimentManager
from main import Main

class TestScienceExperimentPlanner(unittest.TestCase):

    def setUp(self):
        # Setup a temporary directory for experiments
        self.experiment_dir = 'experiments'
        if not os.path.exists(self.experiment_dir):
            os.makedirs(self.experiment_dir)
        self.main_app = Main()

    def tearDown(self):
        # Clean up the temporary directory after tests
        for filename in os.listdir(self.experiment_dir):
            file_path = os.path.join(self.experiment_dir, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_input_and_organize_experiment_details(self):
        # Step 1: Input experiment details
        self.main_app.title_entry.insert(0, "Test Experiment")
        self.main_app.objectives_entry.insert(0, "Test Objectives")
        self.main_app.materials_entry.insert(0, "Test Materials")
        self.main_app.procedures_entry.insert(0, "Test Procedures")
        self.main_app.expected_results_entry.insert(0, "Test Expected Results")
        
        # Step 2: Save the experiment
        self.main_app.add_experiment()
        self.main_app.save_experiment()
        
        # Check if the experiment file is created
        file_path = os.path.join(self.experiment_dir, "Test Experiment.json")
        self.assertTrue(os.path.exists(file_path))
        
        # Load the experiment to verify details
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.assertEqual(data["title"], "Test Experiment")
            self.assertEqual(data["objectives"], "Test Objectives")
            self.assertEqual(data["materials"], "Test Materials")
            self.assertEqual(data["procedures"], "Test Procedures")
            self.assertEqual(data["expected_results"], "Test Expected Results")

    def test_track_progress_of_ongoing_experiments(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality to track progress of ongoing experiments is not implemented")

    def test_record_observations_and_results(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality to record observations and results is not implemented")

    def test_user_friendly_interface_for_managing_multiple_experiments(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality for a user-friendly interface for managing multiple experiments is not implemented")

if __name__ == '__main__':
    unittest.main()
