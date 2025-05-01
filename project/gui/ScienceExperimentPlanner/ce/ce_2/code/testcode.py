import unittest
import os
from main import ExperimentManager, Experiment

class TestExperimentManager(unittest.TestCase):

    def setUp(self):
        self.manager = ExperimentManager()
        self.test_experiment_details = "Experiment 1|water, salt|Mix water and salt"
        self.manager.add_experiment(self.test_experiment_details)

    def test_input_and_organize_experiment_details(self):
        # Functionality 1: Input and Organize Experiment Details
        self.assertEqual(len(self.manager.experiments), 1)
        self.assertEqual(self.manager.experiments[0].objectives, "Experiment 1")
        self.assertEqual(self.manager.experiments[0].materials, ["water", " salt"])
        self.assertEqual(self.manager.experiments[0].procedures, "Mix water and salt")
        
        # Simulate saving and loading experiments
        self.manager.save_experiments()
        self.manager.experiments.clear()
        self.manager.load_experiments()
        self.assertEqual(len(self.manager.experiments), 1)

    def test_track_progress_of_ongoing_experiments(self):
        # Functionality 2: Track Progress of Ongoing Experiments
        self.manager.track_progress(0, "Completed")
        self.assertEqual(self.manager.experiments[0].status, "Completed")

        # Attempt to update status of a non-existing experiment
        with self.assertRaises(IndexError):
            self.manager.track_progress(1, "Completed")

    def test_record_observations_and_results(self):
        # Functionality 3: Record Observations and Results
        observation = "First observation"
        self.manager.experiments[0].record_observation(observation)
        
        # Check if the observation is recorded
        with open("observations.txt", "r") as obs_file:
            lines = obs_file.readlines()
            self.assertIn(f"Experiment 1|{observation}\n", lines)

        # Simulate loading observations (not implemented)
        self.fail("Loading observations functionality not implemented")

    def test_user_friendly_interface_for_managing_multiple_experiments(self):
        # Functionality 4: User-Friendly Interface for Managing Multiple Experiments
        self.manager.add_experiment("Experiment 2|vinegar, baking soda|Combine vinegar and baking soda")
        self.assertEqual(len(self.manager.experiments), 2)

        # Simulate searching (not implemented)
        self.fail("Search functionality not implemented")

if __name__ == '__main__':
    unittest.main()
