import unittest
import os
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
from experiment_manager import ExperimentManager
from main import Main

class TestScienceExperimentPlanner(unittest.TestCase):

    def setUp(self):
        # Set up the Tkinter root and the Main application
        self.root = tk.Tk()
        self.app = Main(self.root)

    def tearDown(self):
        # Destroy the Tkinter root after each test
        self.root.destroy()

    def test_input_and_organize_experiment_details(self):
        # Step 1: Input experiment details
        self.app.title_entry.insert(0, "Test Experiment")
        self.app.objectives_entry.insert("1.0", "Test Objectives")
        self.app.materials_entry.insert("1.0", "Test Materials")
        self.app.procedures_entry.insert("1.0", "Test Procedures")

        # Step 2: Save the experiment
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.add_experiment()
            mock_info.assert_called_with("Success", "Experiment added successfully!")

        # Step 3: View the experiments
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.app.view_experiments()
            mock_info.assert_called_with("Experiments", "Title: Test Experiment\nObjectives: Test Objectives\nMaterials: Test Materials\nProcedures: Test Procedures\nObservations: \nProgress: \n")

    def test_track_progress_of_ongoing_experiments(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality to track progress of ongoing experiments is not implemented.")

    def test_record_observations_and_results(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality to record observations and results is not implemented.")

    def test_user_friendly_interface_for_managing_multiple_experiments(self):
        # Functionality not implemented in the codebase
        self.fail("Functionality for user-friendly interface for managing multiple experiments is not implemented.")

if __name__ == '__main__':
    unittest.main()
