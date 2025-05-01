import unittest
import os
from experiments import Experiment, ExperimentManager

class TestExperimentManager(unittest.TestCase):

    def setUp(self):
        self.manager = ExperimentManager()
        self.manager.load_experiments()

    def test_add_experiment(self):
        # Functionality 1: Input and Organize Experiment Details
        experiment = Experiment("New Experiment", "Test objectives", ["Material 1", "Material 2"], "Test procedures")
        self.manager.add_experiment(experiment)
        self.assertEqual(len(self.manager.experiments), 3)  # Assuming there were 2 experiments initially
        self.assertEqual(self.manager.experiments[-1].title, "New Experiment")

    def test_edit_experiment(self):
        # Functionality 1: Edit an existing experiment
        updated_experiment = Experiment("Updated Experiment", "Updated objectives", ["Material A"], "Updated procedures")
        self.manager.edit_experiment(0, updated_experiment)
        self.assertEqual(self.manager.experiments[0].title, "Updated Experiment")

    def test_delete_experiment(self):
        # Functionality 1: Delete an existing experiment
        self.manager.delete_experiment(0)
        self.assertEqual(len(self.manager.experiments), 1)  # One experiment should be deleted

    def test_update_status(self):
        # Functionality 2: Track Progress of Ongoing Experiments
        experiment = self.manager.experiments[0]
        experiment.update_status("In Progress")
        self.assertEqual(experiment.status, "In Progress")

        # Attempt to update status of a non-ongoing experiment
        with self.assertRaises(IndexError):
            self.manager.edit_experiment(10, experiment)  # Invalid index

    def test_record_observation(self):
        # Functionality 3: Record Observations and Results
        experiment = self.manager.experiments[0]
        experiment.record_observation("First observation")
        self.assertEqual(len(experiment.observations), 1)
        self.assertEqual(experiment.observations[0], "First observation")

    def test_user_friendly_interface(self):
        # Functionality 4: User-Friendly Interface for Managing Multiple Experiments
        self.assertTrue(isinstance(self.manager.experiments, list))
        self.assertGreater(len(self.manager.experiments), 0)  # Ensure there are experiments loaded

        # Simulate searching (not implemented, so we will fail this test)
        self.fail("Search functionality not implemented")

if __name__ == '__main__':
    unittest.main()
