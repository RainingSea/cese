import unittest
import os
from data_manager import DataManager

class TestMedicalHealthTracker(unittest.TestCase):

    def setUp(self):
        # Setup temporary files for testing
        self.activities_file = 'test_activities.txt'
        self.exercise_file = 'test_exercise.txt'
        self.sleep_file = 'test_sleep.txt'
        self.nutrition_file = 'test_nutrition.txt'
        self.stress_file = 'test_stress.txt'

        self.data_manager = DataManager(
            self.activities_file,
            self.exercise_file,
            self.sleep_file,
            self.nutrition_file,
            self.stress_file
        )

    def tearDown(self):
        # Clean up temporary files after each test
        for file in [
            self.activities_file,
            self.exercise_file,
            self.sleep_file,
            self.nutrition_file,
            self.stress_file
        ]:
            if os.path.exists(file):
                os.remove(file)

    def test_input_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        activity = "Walking for 30 minutes"
        self.data_manager.save_activity(activity)
        activities = self.data_manager.load_activities()
        self.assertIn(activity, activities)

    def test_record_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        exercise = "Running for 45 minutes"
        self.data_manager.save_exercise(exercise)
        exercises = self.data_manager.load_exercises()
        self.assertIn(exercise, exercises)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        sleep = "10:00 PM to 6:00 AM"
        self.data_manager.save_sleep(sleep)
        sleep_patterns = self.data_manager.load_sleep()
        self.assertIn(sleep, sleep_patterns)

    def test_track_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        nutrition = "Lunch: Salad, 300 calories"
        self.data_manager.save_nutrition(nutrition)
        nutrition_entries = self.data_manager.load_nutrition()
        self.assertIn(nutrition, nutrition_entries)

    def test_monitor_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        stress = "Stress level 5, feeling okay"
        self.data_manager.save_stress(stress)
        stress_levels = self.data_manager.load_stress()
        self.assertIn(stress, stress_levels)

    def test_provide_visualizations_for_health_trends_analysis(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # Since visualizations are not implemented, this test will fail
        self.fail("Visualizations functionality not implemented")

if __name__ == '__main__':
    unittest.main()
