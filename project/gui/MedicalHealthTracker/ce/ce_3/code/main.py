import tkinter as tk
from tkinter import messagebox
from health_tracker import HealthTracker

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Health Tracker")
        self.health_tracker = HealthTracker(data_directory=".")

        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        daily_activities_menu = tk.Menu(menu)
        menu.add_cascade(label='Daily Activities', menu=daily_activities_menu)
        daily_activities_menu.add_command(label='Input Activity', command=self.input_daily_activity)

        exercise_menu = tk.Menu(menu)
        menu.add_cascade(label='Exercise', menu=exercise_menu)
        exercise_menu.add_command(label='Input Exercise', command=self.input_exercise_routine)

        sleep_menu = tk.Menu(menu)
        menu.add_cascade(label='Sleep', menu=sleep_menu)
        sleep_menu.add_command(label='Log Sleep', command=self.log_sleep_pattern)

        nutrition_menu = tk.Menu(menu)
        menu.add_cascade(label='Nutrition', menu=nutrition_menu)
        nutrition_menu.add_command(label='Track Nutrition', command=self.track_nutrition)

        stress_menu = tk.Menu(menu)
        menu.add_cascade(label='Stress Levels', menu=stress_menu)
        stress_menu.add_command(label='Monitor Stress', command=self.monitor_stress_level)

        menu.add_command(label='Visualize Trends', command=self.visualize_health_trends)

    def input_daily_activity(self):
        activity = self.prompt_user_input("Enter daily activity:")
        if activity:
            self.health_tracker.input_daily_activity(activity)

    def input_exercise_routine(self):
        exercise = self.prompt_user_input("Enter exercise routine:")
        if exercise:
            self.health_tracker.input_exercise_routine(exercise)

    def log_sleep_pattern(self):
        sleep_data = self.prompt_user_input("Enter sleep pattern:")
        if sleep_data:
            self.health_tracker.log_sleep_pattern(sleep_data)

    def track_nutrition(self):
        nutrition_data = self.prompt_user_input("Enter nutrition intake:")
        if nutrition_data:
            self.health_tracker.track_nutrition(nutrition_data)

    def monitor_stress_level(self):
        stress_data = self.prompt_user_input("Enter stress level:")
        if stress_data:
            self.health_tracker.monitor_stress_level(stress_data)

    def visualize_health_trends(self):
        self.health_tracker.visualize_health_trends()

    def prompt_user_input(self, prompt: str) -> str:
        return tk.simpledialog.askstring("Input", prompt)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()