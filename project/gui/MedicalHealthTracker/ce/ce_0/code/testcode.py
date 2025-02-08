import unittest
import os
from health_tracker import HealthTracker

class TestHealthTracker(unittest.TestCase):

    def setUp(self):
        # Set up a new HealthTracker instance before each test
        self.tracker = HealthTracker()
        # Clear data files to ensure a clean state
        open('activities.txt', 'w').close()
        open('exercise.txt', 'w').close()
        open('sleep.txt', 'w').close()
        open('nutrition.txt', 'w').close()
        open('stress.txt', 'w').close()

    def test_input_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        self.tracker.log_activity("Walking for 30 minutes")
        self.tracker.log_activity("Cooking for 1 hour")
        self.tracker.log_activity("Reading for 45 minutes")
        self.tracker.load_data()
        self.assertIn("Walking for 30 minutes", self.tracker.activities)
        self.assertIn("Cooking for 1 hour", self.tracker.activities)
        self.assertIn("Reading for 45 minutes", self.tracker.activities)

    def test_record_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        self.tracker.log_exercise("Running for 20 minutes")
        self.tracker.log_exercise("Weightlifting for 1 hour")
        self.tracker.load_data()
        self.assertIn("Running for 20 minutes", self.tracker.exercise)
        self.assertIn("Weightlifting for 1 hour", self.tracker.exercise)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        self.tracker.log_sleep("10:00 PM to 6:00 AM")
        self.tracker.log_sleep("11:00 PM to 7:00 AM")
        self.tracker.load_data()
        self.assertIn("10:00 PM to 6:00 AM", self.tracker.sleep)
        self.assertIn("11:00 PM to 7:00 AM", self.tracker.sleep)

    def test_track_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        self.tracker.log_nutrition("Breakfast: Oatmeal, 150 calories")
        self.tracker.log_nutrition("Lunch: Salad, 300 calories")
        self.tracker.load_data()
        self.assertIn("Breakfast: Oatmeal, 150 calories", self.tracker.nutrition)
        self.assertIn("Lunch: Salad, 300 calories", self.tracker.nutrition)

    def test_monitor_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        self.tracker.log_stress("Stress level 5, feeling okay")
        self.tracker.log_stress("Stress level 8, very stressed")
        self.tracker.load_data()
        self.assertIn("Stress level 5, feeling okay", self.tracker.stress)
        self.assertIn("Stress level 8, very stressed", self.tracker.stress)

    def test_provide_visualizations_for_health_trends_analysis(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # Since the method only prints data, we will just call it to ensure no exceptions
        try:
            self.tracker.visualize_trends()
        except Exception as e:
            self.fail(f"visualize_trends raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
