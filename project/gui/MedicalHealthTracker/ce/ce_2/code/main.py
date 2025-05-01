import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Health Tracker")
        self.create_frames()
        self.root.mainloop()

    def create_frames(self):
        self.daily_activities_frame = DailyActivities(self.root)
        self.exercise_routines_frame = ExerciseRoutines(self.root)
        self.sleep_patterns_frame = SleepPatterns(self.root)
        self.nutrition_intake_frame = NutritionIntake(self.root)
        self.stress_levels_frame = StressLevels(self.root)
        self.visualizations_frame = Visualizations(self.root)

class DailyActivities:
    def __init__(self, master):
        self.master = master
        self.activities = ""
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.text_area = tk.Text(self.frame, height=5, width=40)
        self.text_area.pack()
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.log_activity)
        self.submit_button.pack()

    def log_activity(self):
        self.activities = self.text_area.get("1.0", tk.END).strip()
        with open("daily_activities.txt", "a") as file:
            file.write(self.activities + "\n")
        messagebox.showinfo("Info", "Daily activities logged successfully!")

class ExerciseRoutines:
    def __init__(self, master):
        self.master = master
        self.exercises = ""
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.text_area = tk.Text(self.frame, height=5, width=40)
        self.text_area.pack()
        self.log_button = tk.Button(self.frame, text="Log Exercise", command=self.log_exercise)
        self.log_button.pack()

    def log_exercise(self):
        self.exercises = self.text_area.get("1.0", tk.END).strip()
        with open("exercise_routines.txt", "a") as file:
            file.write(self.exercises + "\n")
        messagebox.showinfo("Info", "Exercise routines logged successfully!")

class SleepPatterns:
    def __init__(self, master):
        self.master = master
        self.sleep_data = ""
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.text_area = tk.Text(self.frame, height=5, width=40)
        self.text_area.pack()
        self.log_button = tk.Button(self.frame, text="Log Sleep", command=self.log_sleep)
        self.log_button.pack()

    def log_sleep(self):
        self.sleep_data = self.text_area.get("1.0", tk.END).strip()
        with open("sleep_patterns.txt", "a") as file:
            file.write(self.sleep_data + "\n")
        messagebox.showinfo("Info", "Sleep patterns logged successfully!")

class NutritionIntake:
    def __init__(self, master):
        self.master = master
        self.nutrition_data = ""
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.text_area = tk.Text(self.frame, height=5, width=40)
        self.text_area.pack()
        self.log_button = tk.Button(self.frame, text="Log Nutrition", command=self.log_nutrition)
        self.log_button.pack()

    def log_nutrition(self):
        self.nutrition_data = self.text_area.get("1.0", tk.END).strip()
        with open("nutrition_intake.txt", "a") as file:
            file.write(self.nutrition_data + "\n")
        messagebox.showinfo("Info", "Nutrition intake logged successfully!")

class StressLevels:
    def __init__(self, master):
        self.master = master
        self.stress_data = ""
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.text_area = tk.Text(self.frame, height=5, width=40)
        self.text_area.pack()
        self.log_button = tk.Button(self.frame, text="Log Stress", command=self.log_stress)
        self.log_button.pack()

    def log_stress(self):
        self.stress_data = self.text_area.get("1.0", tk.END).strip()
        with open("stress_levels.txt", "a") as file:
            file.write(self.stress_data + "\n")
        messagebox.showinfo("Info", "Stress levels logged successfully!")

class Visualizations:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.plot_button = tk.Button(self.frame, text="Generate Trends", command=self.generate_trends)
        self.plot_button.pack()

    def generate_trends(self):
        # Placeholder for trend generation logic
        messagebox.showinfo("Info", "Trend generation feature is under development.")

if __name__ == "__main__":
    Main()