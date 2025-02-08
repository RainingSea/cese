import unittest
import os
from tkinter import Tk
from main import Main
from experiment import Experiment
from experiment_manager import ExperimentManager

class TestScienceExperimentPlanner(unittest.TestCase):

    def setUp(self):
        # Set up the application environment
        self.root = Tk()
        self.app = Main(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_input_and_organize_experiment_details(self):
        # Simulate adding a new experiment
        self.app.create_experiment()
        experiment_window = self.root.winfo_children()[-1]  # Get the topmost window
        entries = experiment_window.winfo_children()

        # Fill in the fields
        entries[1].insert(0, "Test Objective")
        entries[3].insert(0, "Test Materials")
        entries[5].insert(0, "Test Procedure")

        # Simulate clicking the "Save" button
        entries[6].invoke()

        # Check if the experiment was saved
        experiments = self.app.experiment_manager.get_experiments()
        self.assertEqual(len(experiments), 3)  # Assuming there were initially 2 experiments
        self.assertEqual(experiments[-1].objective, "Test Objective")
        self.assertEqual(experiments[-1].materials, "Test Materials")
        self.assertEqual(experiments[-1].procedure, "Test Procedure")

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
