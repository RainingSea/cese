import unittest
from data_handler import DataHandler
from activity import Activity
from exercise import Exercise
from sleep import Sleep
from nutrition import Nutrition
from stress import Stress
import os

class TestMedicalHealthTracker(unittest.TestCase):

    def setUp(self):
        # Setup temporary files for testing
        self.activity_file = 'test_activities.txt'
        self.exercise_file = 'test_exercise.txt'
        self.sleep_file = 'test_sleep.txt'
        self.nutrition_file = 'test_nutrition.txt'
        self.stress_file = 'test_stress.txt'
        
        # Initialize DataHandler for each file
        self.activity_data_handler = DataHandler(self.activity_file)
        self.exercise_data_handler = DataHandler(self.exercise_file)
        self.sleep_data_handler = DataHandler(self.sleep_file)
        self.nutrition_data_handler = DataHandler(self.nutrition_file)
        self.stress_data_handler = DataHandler(self.stress_file)

    def tearDown(self):
        # Remove temporary files after tests
        if os.path.exists(self.activity_file):
            os.remove(self.activity_file)
        if os.path.exists(self.exercise_file):
            os.remove(self.exercise_file)
        if os.path.exists(self.sleep_file):
            os.remove(self.sleep_file)
        if os.path.exists(self.nutrition_file):
            os.remove(self.nutrition_file)
        if os.path.exists(self.stress_file):
            os.remove(self.stress_file)

    def test_input_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        activity = Activity("2023-10-03", "Reading for 1 hour")
        self.activity_data_handler.write_data(f"{activity.date}: {activity.description}")
        data = self.activity_data_handler.read_data()
        self.assertIn("2023-10-03: Reading for 1 hour\n", data)

    def test_record_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        exercise = Exercise("2023-10-03", "Cycling for 30 minutes")
        self.exercise_data_handler.write_data(f"{exercise.date}: {exercise.description}")
        data = self.exercise_data_handler.read_data()
        self.assertIn("2023-10-03: Cycling for 30 minutes\n", data)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        sleep = Sleep("2023-10-03", "8 hours")
        self.sleep_data_handler.write_data(f"{sleep.date}: {sleep.duration}")
        data = self.sleep_data_handler.read_data()
        self.assertIn("2023-10-03: 8 hours\n", data)

    def test_track_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        nutrition = Nutrition("2023-10-03", "Breakfast: Eggs, Lunch: Salad, Dinner: Fish")
        self.nutrition_data_handler.write_data(f"{nutrition.date}: {nutrition.meal_info}")
        data = self.nutrition_data_handler.read_data()
        self.assertIn("2023-10-03: Breakfast: Eggs, Lunch: Salad, Dinner: Fish\n", data)

    def test_monitor_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        stress = Stress("2023-10-03", "High")
        self.stress_data_handler.write_data(f"{stress.date}: {stress.level}")
        data = self.stress_data_handler.read_data()
        self.assertIn("2023-10-03: High\n", data)

    def test_provide_visualizations_for_health_trends_analysis(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # This functionality is not directly testable via unit tests as it involves GUI rendering.
        # We will assume this is not implemented in the current codebase.
        self.fail("Visualization functionality not implemented")

if __name__ == '__main__':
    unittest.main()
