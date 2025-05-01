import tkinter as tk
from tkinter import messagebox
from data_manager import DataManager
import matplotlib.pyplot as plt

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ui = UI(self.data_manager)

    def main(self):
        self.data_manager.load_data()
        self.ui.show_main_menu()
        tk.mainloop()

class UI:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.root = tk.Tk()
        self.root.title("Medical Health Tracker")

    def show_main_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        activities_menu = tk.Menu(menu)
        menu.add_cascade(label="Daily Activities", menu=activities_menu)
        activities_menu.add_command(label="Input", command=self.input_daily_activity)

        exercise_menu = tk.Menu(menu)
        menu.add_cascade(label="Exercise Routines", menu=exercise_menu)
        exercise_menu.add_command(label="Input", command=self.input_exercise_routine)

        sleep_menu = tk.Menu(menu)
        menu.add_cascade(label="Sleep Patterns", menu=sleep_menu)
        sleep_menu.add_command(label="Input", command=self.input_sleep_pattern)

        nutrition_menu = tk.Menu(menu)
        menu.add_cascade(label="Nutrition Intake", menu=nutrition_menu)
        nutrition_menu.add_command(label="Input", command=self.input_nutrition_intake)

        stress_menu = tk.Menu(menu)
        menu.add_cascade(label="Stress Levels", menu=stress_menu)
        stress_menu.add_command(label="Input", command=self.input_stress_level)

        menu.add_command(label="Summary", command=self.show_summary)
        menu.add_command(label="Visualize Activities", command=self.generate_visualizations)

    def input_daily_activity(self):
        self._input_data("Daily Activity", self.data_manager.save_daily_activity)

    def input_exercise_routine(self):
        self._input_data("Exercise Routine", self.data_manager.save_exercise_routine)

    def input_sleep_pattern(self):
        self._input_data("Sleep Pattern", self.data_manager.save_sleep_pattern)

    def input_nutrition_intake(self):
        self._input_data("Nutrition Intake", self.data_manager.save_nutrition_intake)

    def input_stress_level(self):
        self._input_data("Stress Level", self.data_manager.save_stress_level)

    def _input_data(self, title, save_function):
        def save():
            data = entry.get()
            if data:
                save_function(data)
                messagebox.showinfo("Success", f"{title} saved successfully!")
                input_window.destroy()
            else:
                messagebox.showerror("Error", "Input cannot be empty.")

        input_window = tk.Toplevel(self.root)
        input_window.title(title)
        tk.Label(input_window, text=f"Enter {title}:").pack()
        entry = tk.Entry(input_window)
        entry.pack()
        tk.Button(input_window, text="Submit", command=save).pack()

    def show_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Summary")
        summary_text = tk.Text(summary_window)
        summary_text.pack()

        for activity in self.data_manager.daily_activities:
            summary_text.insert(tk.END, f"{activity}\n")
        for exercise in self.data_manager.exercise_routines:
            summary_text.insert(tk.END, f"{exercise}\n")
        for sleep in self.data_manager.sleep_patterns:
            summary_text.insert(tk.END, f"{sleep}\n")
        for nutrition in self.data_manager.nutrition_intake:
            summary_text.insert(tk.END, f"{nutrition}\n")
        for stress in self.data_manager.stress_levels:
            summary_text.insert(tk.END, f"{stress}\n")

    def generate_visualizations(self):
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(self.data_manager.daily_activities)), self.data_manager.daily_activities, marker='o')
        plt.title('Daily Activities')
        plt.xlabel('Days')
        plt.ylabel('Activities')
        plt.xticks(range(len(self.data_manager.daily_activities)), self.data_manager.daily_activities, rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = Main()
    app.main()