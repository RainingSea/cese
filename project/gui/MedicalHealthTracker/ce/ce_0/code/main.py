import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class HealthTracker:
    def __init__(self):
        self.daily_activities = []
        self.exercise_routines = []
        self.sleep_patterns = []
        self.nutrition_intake = []
        self.stress_levels = []

    def log_activity(self, activity: str):
        self.daily_activities.append(activity)
        self._save_to_file("daily_activities.txt", activity)

    def log_exercise(self, exercise: str):
        self.exercise_routines.append(exercise)
        self._save_to_file("exercise_routines.txt", exercise)

    def log_sleep(self, sleep: str):
        self.sleep_patterns.append(sleep)
        self._save_to_file("sleep_patterns.txt", sleep)

    def log_nutrition(self, nutrition: str):
        self.nutrition_intake.append(nutrition)
        self._save_to_file("nutrition_intake.txt", nutrition)

    def log_stress(self, stress: str):
        self.stress_levels.append(stress)
        self._save_to_file("stress_levels.txt", stress)

    def generate_visualizations(self):
        # Example visualization for daily activities
        plt.figure(figsize=(10, 5))
        plt.plot(self.daily_activities, marker='o')
        plt.title('Daily Activities')
        plt.xlabel('Days')
        plt.ylabel('Activities')
        plt.show()

    def _save_to_file(self, filename: str, data: str):
        with open(filename, 'a') as file:
            file.write(data + '\n')

class Main:
    def __init__(self, root):
        self.health_tracker = HealthTracker()
        self.root = root
        self.root.title("Medical Health Tracker")

        self.create_widgets()

    def create_widgets(self):
        self.activity_entry = tk.Entry(self.root)
        self.activity_entry.pack()
        self.activity_button = tk.Button(self.root, text="Log Activity", command=self.log_activity)
        self.activity_button.pack()

        self.exercise_entry = tk.Entry(self.root)
        self.exercise_entry.pack()
        self.exercise_button = tk.Button(self.root, text="Log Exercise", command=self.log_exercise)
        self.exercise_button.pack()

        self.sleep_entry = tk.Entry(self.root)
        self.sleep_entry.pack()
        self.sleep_button = tk.Button(self.root, text="Log Sleep", command=self.log_sleep)
        self.sleep_button.pack()

        self.nutrition_entry = tk.Entry(self.root)
        self.nutrition_entry.pack()
        self.nutrition_button = tk.Button(self.root, text="Log Nutrition", command=self.log_nutrition)
        self.nutrition_button.pack()

        self.stress_entry = tk.Entry(self.root)
        self.stress_entry.pack()
        self.stress_button = tk.Button(self.root, text="Log Stress", command=self.log_stress)
        self.stress_button.pack()

        self.visualize_button = tk.Button(self.root, text="Generate Visualizations", command=self.generate_visualizations)
        self.visualize_button.pack()

    def log_activity(self):
        activity = self.activity_entry.get()
        if activity:
            self.health_tracker.log_activity(activity)
            messagebox.showinfo("Info", "Activity logged successfully!")
            self.activity_entry.delete(0, tk.END)

    def log_exercise(self):
        exercise = self.exercise_entry.get()
        if exercise:
            self.health_tracker.log_exercise(exercise)
            messagebox.showinfo("Info", "Exercise logged successfully!")
            self.exercise_entry.delete(0, tk.END)

    def log_sleep(self):
        sleep = self.sleep_entry.get()
        if sleep:
            self.health_tracker.log_sleep(sleep)
            messagebox.showinfo("Info", "Sleep pattern logged successfully!")
            self.sleep_entry.delete(0, tk.END)

    def log_nutrition(self):
        nutrition = self.nutrition_entry.get()
        if nutrition:
            self.health_tracker.log_nutrition(nutrition)
            messagebox.showinfo("Info", "Nutrition logged successfully!")
            self.nutrition_entry.delete(0, tk.END)

    def log_stress(self):
        stress = self.stress_entry.get()
        if stress:
            self.health_tracker.log_stress(stress)
            messagebox.showinfo("Info", "Stress level logged successfully!")
            self.stress_entry.delete(0, tk.END)

    def generate_visualizations(self):
        self.health_tracker.generate_visualizations()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()