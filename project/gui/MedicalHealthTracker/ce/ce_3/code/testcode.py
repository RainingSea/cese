import unittest
import os
from health_tracker import HealthTracker

class TestHealthTracker(unittest.TestCase):

    def setUp(self):
        self.data_directory = "./test_data"
        os.makedirs(self.data_directory, exist_ok=True)
        self.health_tracker = HealthTracker(data_directory=self.data_directory)

    def tearDown(self):
        # Clean up the test data directory after each test
        for file_name in os.listdir(self.data_directory):
            file_path = os.path.join(self.data_directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.data_directory)

    def test_input_daily_activity(self):
        # Functionalities 1: Input Daily Activities
        activity = "Walked 5,000 steps"
        self.health_tracker.input_daily_activity(activity)
        with open(self.health_tracker.daily_activities_file, 'r') as file:
            data = file.read()
        self.assertIn(activity, data)

    def test_input_exercise_routine(self):
        # Functionalities 2: Record Exercise Routines
        exercise = "Cycling for 30 minutes"
        self.health_tracker.input_exercise_routine(exercise)
        with open(self.health_tracker.exercise_routines_file, 'r') as file:
            data = file.read()
        self.assertIn(exercise, data)

    def test_log_sleep_pattern(self):
        # Functionalities 3: Log Sleep Patterns
        sleep_data = "Slept from 11:00 PM to 7:00 AM"
        self.health_tracker.log_sleep_pattern(sleep_data)
        with open(self.health_tracker.sleep_patterns_file, 'r') as file:
            data = file.read()
        self.assertIn(sleep_data, data)

    def test_track_nutrition(self):
        # Functionalities 4: Track Nutrition Intake
        nutrition_data = "Lunch: Salad with chicken"
        self.health_tracker.track_nutrition(nutrition_data)
        with open(self.health_tracker.nutrition_intake_file, 'r') as file:
            data = file.read()
        self.assertIn(nutrition_data, data)

    def test_monitor_stress_level(self):
        # Functionalities 5: Monitor Stress Levels
        stress_data = "Stress level: 5 (1-10 scale)"
        self.health_tracker.monitor_stress_level(stress_data)
        with open(self.health_tracker.stress_levels_file, 'r') as file:
            data = file.read()
        self.assertIn(stress_data, data)

    def test_visualize_health_trends(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # Since the visualization is a placeholder, we will just check the print statement
        with self.assertLogs() as log:
            self.health_tracker.visualize_health_trends()
        self.assertIn("Visualizing health trends...", log.output[0])

if __name__ == '__main__':
    unittest.main()
