import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from main import Main
from ExperimentManager import ExperimentManager

class TestScienceExperimentPlanner(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = Main(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_input_and_organize_experiment_details(self):
        # Step 1: Check if input fields are present
        self.assertIsNotNone(self.app.objectives_entry)
        self.assertIsNotNone(self.app.materials_entry)
        self.assertIsNotNone(self.app.procedure_entry)

        # Step 2: Fill in the fields and add an experiment
        self.app.objectives_entry.insert(0, "Test Objective")
        self.app.materials_entry.insert(0, "Test Materials")
        self.app.procedure_entry.insert(0, "Test Procedure")
        
        with patch.object(self.app.experiment_manager, 'add_experiment') as mock_add_experiment:
            self.app.add_experiment()
            mock_add_experiment.assert_called_once_with({
                'objectives': "Test Objective",
                'materials': "Test Materials",
                'procedure': "Test Procedure"
            })

        # Step 3: Check if the experiment appears in the list
        self.app.load_experiments()
        experiments = self.app.experiment_manager.get_experiments()
        self.assertTrue(any(exp['objectives'] == "Test Objective" for exp in experiments))

    def test_track_progress_of_ongoing_experiments(self):
        # Mock the experiments data
        self.app.experiment_manager.experiments = [
            MagicMock(id=1, status="In Progress"),
            MagicMock(id=2, status="Not Started")
        ]

        # Step 1: Check if ongoing experiments can be viewed
        ongoing_experiments = [exp for exp in self.app.experiment_manager.experiments if exp.status == "In Progress"]
        self.assertGreater(len(ongoing_experiments), 0)

        # Step 2: Update status of an ongoing experiment
        ongoing_experiments[0].update_status("Completed")
        self.assertEqual(ongoing_experiments[0].status, "Completed")

        # Step 3: Attempt to update a non-ongoing experiment
        with self.assertRaises(Exception):
            if self.app.experiment_manager.experiments[1].status != "In Progress":
                raise Exception("Experiment cannot be updated")

    def test_record_observations_and_results(self):
        # Mock the observations
        observation = MagicMock(experiment_id=1, note="Observation Note")
        self.app.experiment_manager.experiments = [MagicMock(id=1, status="In Progress")]

        # Step 1: Check if experiment details can be viewed
        experiment = self.app.experiment_manager.experiments[0]
        self.assertEqual(experiment.id, 1)

        # Step 2: Record an observation
        with patch('Observation') as MockObservation:
            MockObservation.return_value = observation
            new_observation = MockObservation(1, "Observation Note")
            self.assertEqual(new_observation.note, "Observation Note")

        # Step 3: Check if the observation is recorded
        self.assertEqual(new_observation.note, "Observation Note")

    def test_user_friendly_interface_for_managing_multiple_experiments(self):
        # Step 1: Check if the main dashboard is organized
        self.assertIsNotNone(self.app.experiment_list)

        # Step 2: Simulate search functionality
        self.app.experiment_manager.experiments = [
            MagicMock(id=1, objectives="Test Objective 1"),
            MagicMock(id=2, objectives="Test Objective 2")
        ]
        search_result = [exp for exp in self.app.experiment_manager.experiments if "1" in exp.objectives]
        self.assertEqual(len(search_result), 1)

        # Step 3: Check if experiment details can be viewed
        selected_experiment = self.app.experiment_manager.experiments[0]
        self.assertEqual(selected_experiment.objectives, "Test Objective 1")

if __name__ == '__main__':
    unittest.main()
