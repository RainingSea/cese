import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Health Tracker")
        self.activity_tracker = ActivityTracker()
        self.exercise_logger = ExerciseLogger()
        self.sleep_logger = SleepLogger()
        self.nutrition_tracker = NutritionTracker()
        self.stress_monitor = StressMonitor()
        self.create_menu()
        
    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        health_menu = tk.Menu(menu)
        menu.add_cascade(label="Health", menu=health_menu)
        health_menu.add_command(label="Daily Activities", command=self.open_activities)
        health_menu.add_command(label="Exercise", command=self.open_exercise)
        health_menu.add_command(label="Sleep", command=self.open_sleep)
        health_menu.add_command(label="Nutrition", command=self.open_nutrition)
        health_menu.add_command(label="Stress", command=self.open_stress)
        health_menu.add_command(label="Visualizations", command=self.open_visualizations)
        
    def open_activities(self):
        self.open_input_window("Activities", self.activity_tracker.add_activity, "activity")
        
    def open_exercise(self):
        self.open_input_window("Exercise", self.exercise_logger.log_exercise, "exercise")
        
    def open_sleep(self):
        self.open_input_window("Sleep", self.sleep_logger.log_sleep, "sleep")
        
    def open_nutrition(self):
        self.open_input_window("Nutrition", self.nutrition_tracker.track_nutrition, "nutrition")
        
    def open_stress(self):
        self.open_input_window("Stress", self.stress_monitor.monitor_stress, "stress")
        
    def open_input_window(self, title, log_function, data_type):
        input_window = tk.Toplevel(self.root)
        input_window.title(title)
        
        tk.Label(input_window, text=f"Enter {data_type}:").pack()
        entry = tk.Entry(input_window)
        entry.pack()
        
        tk.Label(input_window, text="Enter duration (in minutes):").pack()
        duration_entry = tk.Entry(input_window)
        duration_entry.pack()
        
        tk.Button(input_window, text="Submit", command=lambda: self.submit_data(log_function, entry, duration_entry)).pack()
        
    def submit_data(self, log_function, entry, duration_entry):
        try:
            data = entry.get()
            duration = int(duration_entry.get())
            log_function(data, duration)
            messagebox.showinfo("Success", "Data logged successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid duration.")
        
    def open_visualizations(self):
        plt.figure()
        plt.title("Health Visualizations")
        plt.plot([1, 2, 3], [1, 2, 3])  # Placeholder for actual data
        plt.show()

class ActivityTracker:
    def __init__(self):
        self.activities = []
        
    def add_activity(self, activity: str, duration: int):
        self.activities.append((activity, duration))
        self.save_to_file()
        
    def save_to_file(self):
        with open("activities.txt", "a") as file:
            for activity, duration in self.activities:
                file.write(f"{activity}|{duration}\n")

class ExerciseLogger:
    def __init__(self):
        self.exercises = []
        
    def log_exercise(self, exercise: str, duration: int):
        self.exercises.append((exercise, duration))
        self.save_to_file()
        
    def save_to_file(self):
        with open("exercise.txt", "a") as file:
            for exercise, duration in self.exercises:
                file.write(f"{exercise}|{duration}\n")

class SleepLogger:
    def __init__(self):
        self.sleep_records = []
        
    def log_sleep(self, duration: int):
        self.sleep_records.append(duration)
        self.save_to_file()
        
    def save_to_file(self):
        with open("sleep.txt", "a") as file:
            for duration in self.sleep_records:
                file.write(f"{duration}\n")

class NutritionTracker:
    def __init__(self):
        self.nutrition_entries = []
        
    def track_nutrition(self, food: str, calories: int):
        self.nutrition_entries.append((food, calories))
        self.save_to_file()
        
    def save_to_file(self):
        with open("nutrition.txt", "a") as file:
            for food, calories in self.nutrition_entries:
                file.write(f"{food}|{calories}\n")

class StressMonitor:
    def __init__(self):
        self.stress_levels = []
        
    def monitor_stress(self, level: int):
        self.stress_levels.append(level)
        self.save_to_file()
        
    def save_to_file(self):
        with open("stress.txt", "a") as file:
            for level in self.stress_levels:
                file.write(f"{level}\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()