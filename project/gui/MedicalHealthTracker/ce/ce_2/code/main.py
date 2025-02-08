import tkinter as tk
from tkinter import ttk
from data_manager import DataManager

class Main:
    def __init__(self):
        self.data_manager = DataManager('activities.txt', 'exercise.txt', 'sleep.txt', 'nutrition.txt', 'stress.txt')
        self.root = tk.Tk()
        self.root.title("Medical Health Tracker")
        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.create_daily_activities_tab(tab_control)
        self.create_exercise_routines_tab(tab_control)
        self.create_sleep_patterns_tab(tab_control)
        self.create_nutrition_intake_tab(tab_control)
        self.create_stress_levels_tab(tab_control)
        self.create_visualizations_tab(tab_control)

        tab_control.pack(expand=1, fill='both')

    def create_daily_activities_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Daily Activities')

        self.activity_entry = tk.Entry(tab)
        self.activity_entry.pack(pady=10)

        save_button = tk.Button(tab, text='Save Activity', command=self.save_activity)
        save_button.pack(pady=5)

    def save_activity(self):
        activity = self.activity_entry.get()
        if activity:
            self.data_manager.save_activity(activity)
            self.activity_entry.delete(0, tk.END)

    def create_exercise_routines_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Exercise Routines')

        self.exercise_entry = tk.Entry(tab)
        self.exercise_entry.pack(pady=10)

        save_button = tk.Button(tab, text='Save Exercise', command=self.save_exercise)
        save_button.pack(pady=5)

    def save_exercise(self):
        exercise = self.exercise_entry.get()
        if exercise:
            self.data_manager.save_exercise(exercise)
            self.exercise_entry.delete(0, tk.END)

    def create_sleep_patterns_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Sleep Patterns')

        self.sleep_entry = tk.Entry(tab)
        self.sleep_entry.pack(pady=10)

        save_button = tk.Button(tab, text='Save Sleep', command=self.save_sleep)
        save_button.pack(pady=5)

    def save_sleep(self):
        sleep = self.sleep_entry.get()
        if sleep:
            self.data_manager.save_sleep(sleep)
            self.sleep_entry.delete(0, tk.END)

    def create_nutrition_intake_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Nutrition Intake')

        self.nutrition_entry = tk.Entry(tab)
        self.nutrition_entry.pack(pady=10)

        save_button = tk.Button(tab, text='Save Nutrition', command=self.save_nutrition)
        save_button.pack(pady=5)

    def save_nutrition(self):
        nutrition = self.nutrition_entry.get()
        if nutrition:
            self.data_manager.save_nutrition(nutrition)
            self.nutrition_entry.delete(0, tk.END)

    def create_stress_levels_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Stress Levels')

        self.stress_entry = tk.Entry(tab)
        self.stress_entry.pack(pady=10)

        save_button = tk.Button(tab, text='Save Stress', command=self.save_stress)
        save_button.pack(pady=5)

    def save_stress(self):
        stress = self.stress_entry.get()
        if stress:
            self.data_manager.save_stress(stress)
            self.stress_entry.delete(0, tk.END)

    def create_visualizations_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Visualizations')
        # Visualization logic will be implemented here later

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()