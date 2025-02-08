import unittest
from main import ExperimentManager, ObservationManager, Experiment

class TestScienceExperimentPlanner(unittest.TestCase):

    def setUp(self):
        # Initialize the ExperimentManager and ObservationManager
        self.experiment_manager = ExperimentManager()
        self.observation_manager = ObservationManager()

    def test_input_and_organize_experiment_details(self):
        # Functionalities 1: Input and Organize Experiment Details
        initial_count = len(self.experiment_manager.get_experiments())
        
        # Add a new experiment
        self.experiment_manager.add_experiment(
            "Test Experiment",
            "Test Materials",
            "Test Procedure",
            "Test Expected Results"
        )
        
        # Check if the experiment is added
        self.assertEqual(len(self.experiment_manager.get_experiments()), initial_count + 1)
        
        # Verify the last added experiment details
        last_experiment = self.experiment_manager.get_experiments()[-1]
        self.assertEqual(last_experiment.objective, "Test Experiment")
        self.assertEqual(last_experiment.materials, "Test Materials")
        self.assertEqual(last_experiment.procedure, "Test Procedure")
        self.assertEqual(last_experiment.expected_results, "Test Expected Results")

    def test_track_progress_of_ongoing_experiments(self):
        # Functionalities 2: Track Progress of Ongoing Experiments
        # This functionality is not implemented in the codebase
        self.fail("Track Progress of Ongoing Experiments functionality not implemented")

    def test_record_observations_and_results(self):
        # Functionalities 3: Record Observations and Results
        experiment_id = 1  # Assuming experiment with ID 1 exists
        initial_count = len(self.observation_manager.observations)
        
        # Record a new observation
        self.observation_manager.record_observation(experiment_id, "New Observation")
        
        # Check if the observation is recorded
        self.assertEqual(len(self.observation_manager.observations), initial_count + 1)
        
        # Verify the last recorded observation
        last_observation = self.observation_manager.observations[-1]
        self.assertEqual(last_observation.experiment_id, experiment_id)
        self.assertEqual(last_observation.observation, "New Observation")

    def test_user_friendly_interface_for_managing_multiple_experiments(self):
        # Functionalities 4: User-Friendly Interface for Managing Multiple Experiments
        # This functionality is not implemented in the codebase
        self.fail("User-Friendly Interface for Managing Multiple Experiments functionality not implemented")

if __name__ == '__main__':
    unittest.main()
