import unittest
import os

class TestHealthTracker(unittest.TestCase):

    def setUp(self):
        # Ensure the test files are clean before each test
        self.daily_activities_file = "daily_activities.txt"
        self.exercise_routines_file = "exercise_routines.txt"
        self.sleep_patterns_file = "sleep_patterns.txt"
        self.nutrition_intake_file = "nutrition_intake.txt"
        self.stress_levels_file = "stress_levels.txt"
        
        for file in [self.daily_activities_file, self.exercise_routines_file,
                     self.sleep_patterns_file, self.nutrition_intake_file,
                     self.stress_levels_file]:
            open(file, 'w').close()  # Clear the file content

    def test_log_daily_activities(self):
        # Functionalities 1: Input Daily Activities
        activity = "Went for a walk for 30 minutes"
        with open(self.daily_activities_file, "a") as file:
            file.write(activity + "\n")
        
        with open(self.daily_activities_file, "r") as file:
            activities = file.readlines()
        
        self.assertIn(activity + "\n", activities)

    def test_log_exercise_routines(self):
        # Functionalities 2: Record Exercise Routines
        exercise = "30 minutes of running"
        with open(self.exercise_routines_file, "a") as file:
            file.write(exercise + "\n")
        
        with open(self.exercise_routines_file, "r") as file:
            exercises = file.readlines()
        
        self.assertIn(exercise + "\n", exercises)

    def test_log_sleep_patterns(self):
        # Functionalities 3: Log Sleep Patterns
        sleep_pattern = "Slept for 8 hours from 10 PM to 6 AM"
        with open(self.sleep_patterns_file, "a") as file:
            file.write(sleep_pattern + "\n")
        
        with open(self.sleep_patterns_file, "r") as file:
            sleep_patterns = file.readlines()
        
        self.assertIn(sleep_pattern + "\n", sleep_patterns)

    def test_log_nutrition_intake(self):
        # Functionalities 4: Track Nutrition Intake
        nutrition = "Breakfast: Oatmeal and fruit"
        with open(self.nutrition_intake_file, "a") as file:
            file.write(nutrition + "\n")
        
        with open(self.nutrition_intake_file, "r") as file:
            nutrition_entries = file.readlines()
        
        self.assertIn(nutrition + "\n", nutrition_entries)

    def test_log_stress_levels(self):
        # Functionalities 5: Monitor Stress Levels
        stress_level = "Stress level: 7 - Had a busy day"
        with open(self.stress_levels_file, "a") as file:
            file.write(stress_level + "\n")
        
        with open(self.stress_levels_file, "r") as file:
            stress_levels = file.readlines()
        
        self.assertIn(stress_level + "\n", stress_levels)

    def test_visualizations_feature(self):
        # Functionalities 6: Provide Visualizations for Health Trends Analysis
        # This feature is under development, so we will return a failure
        self.fail("Visualization feature is under development.")

if __name__ == '__main__':
    unittest.main()
