import tkinter as tk
from tkinter import messagebox
from health_tracker import HealthTracker

class Main:
    def __init__(self, master):
        self.master = master
        self.health_tracker = HealthTracker()
        self.master.title("Medical Health Tracker")

        self.create_widgets()

    def create_widgets(self):
        self.activity_label = tk.Label(self.master, text="Log Activity:")
        self.activity_label.pack()
        self.activity_entry = tk.Entry(self.master)
        self.activity_entry.pack()
        self.activity_button = tk.Button(self.master, text="Save Activity", command=self.save_activity)
        self.activity_button.pack()

        self.exercise_label = tk.Label(self.master, text="Log Exercise:")
        self.exercise_label.pack()
        self.exercise_entry = tk.Entry(self.master)
        self.exercise_entry.pack()
        self.exercise_button = tk.Button(self.master, text="Save Exercise", command=self.save_exercise)
        self.exercise_button.pack()

        self.sleep_label = tk.Label(self.master, text="Log Sleep:")
        self.sleep_label.pack()
        self.sleep_entry = tk.Entry(self.master)
        self.sleep_entry.pack()
        self.sleep_button = tk.Button(self.master, text="Save Sleep", command=self.save_sleep)
        self.sleep_button.pack()

        self.nutrition_label = tk.Label(self.master, text="Log Nutrition:")
        self.nutrition_label.pack()
        self.nutrition_entry = tk.Entry(self.master)
        self.nutrition_entry.pack()
        self.nutrition_button = tk.Button(self.master, text="Save Nutrition", command=self.save_nutrition)
        self.nutrition_button.pack()

        self.stress_label = tk.Label(self.master, text="Log Stress:")
        self.stress_label.pack()
        self.stress_entry = tk.Entry(self.master)
        self.stress_entry.pack()
        self.stress_button = tk.Button(self.master, text="Save Stress", command=self.save_stress)
        self.stress_button.pack()

        self.visualize_button = tk.Button(self.master, text="Visualize Trends", command=self.visualize_trends)
        self.visualize_button.pack()

    def save_activity(self):
        activity = self.activity_entry.get()
        if activity:
            self.health_tracker.log_activity(activity)
            messagebox.showinfo("Info", "Activity logged successfully!")
            self.activity_entry.delete(0, tk.END)

    def save_exercise(self):
        exercise = self.exercise_entry.get()
        if exercise:
            self.health_tracker.log_exercise(exercise)
            messagebox.showinfo("Info", "Exercise logged successfully!")
            self.exercise_entry.delete(0, tk.END)

    def save_sleep(self):
        sleep = self.sleep_entry.get()
        if sleep:
            self.health_tracker.log_sleep(sleep)
            messagebox.showinfo("Info", "Sleep logged successfully!")
            self.sleep_entry.delete(0, tk.END)

    def save_nutrition(self):
        nutrition = self.nutrition_entry.get()
        if nutrition:
            self.health_tracker.log_nutrition(nutrition)
            messagebox.showinfo("Info", "Nutrition logged successfully!")
            self.nutrition_entry.delete(0, tk.END)

    def save_stress(self):
        stress = self.stress_entry.get()
        if stress:
            self.health_tracker.log_stress(stress)
            messagebox.showinfo("Info", "Stress logged successfully!")
            self.stress_entry.delete(0, tk.END)

    def visualize_trends(self):
        self.health_tracker.visualize_trends()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()