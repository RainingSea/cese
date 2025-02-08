import tkinter as tk
from tkinter import ttk
from data_handler import DataHandler
from activity import Activity
from exercise import Exercise
from sleep import Sleep
from nutrition import Nutrition
from stress import Stress

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Medical Health Tracker")
        self.data_handler = DataHandler("activities.txt")
        self.create_tabs()
    
    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.daily_activities_tab = ttk.Frame(tab_control)
        tab_control.add(self.daily_activities_tab, text='Daily Activities')
        tab_control.pack(expand=1, fill='both')

        # More tabs can be created similarly...

        self.create_activity_tab()

    def create_activity_tab(self):
        self.activity_input = tk.Entry(self.daily_activities_tab)
        self.activity_input.pack(pady=10)

        log_button = tk.Button(self.daily_activities_tab, text="Log Activity", command=self.log_activity)
        log_button.pack(pady=10)

    def log_activity(self):
        activity_description = self.activity_input.get()
        activity = Activity("2023-10-01", activity_description)  # Example date
        self.data_handler.write_data(f"{activity.date}: {activity.description}")
        self.activity_input.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()