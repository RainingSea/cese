import tkinter as tk
from tkinter import messagebox
import os

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Tracker")
        self.experiment_manager = ExperimentManager()
        self.experiment_manager.load_experiments()
        
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        experiment_menu = tk.Menu(menu)
        menu.add_cascade(label="Experiments", menu=experiment_menu)
        experiment_menu.add_command(label="Create Experiment", command=self.create_experiment)
        experiment_menu.add_command(label="View Experiments", command=self.view_experiments)

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="Welcome to Experiment Tracker")
        self.status_label.pack(pady=20)

    def create_experiment(self):
        experiment_window = tk.Toplevel(self.root)
        experiment_window.title("New Experiment")
        
        tk.Label(experiment_window, text="Objective:").pack()
        objective_entry = tk.Entry(experiment_window)
        objective_entry.pack()

        tk.Label(experiment_window, text="Materials:").pack()
        materials_entry = tk.Entry(experiment_window)
        materials_entry.pack()

        tk.Label(experiment_window, text="Procedure:").pack()
        procedure_entry = tk.Entry(experiment_window)
        procedure_entry.pack()

        tk.Button(experiment_window, text="Save", command=lambda: self.save_experiment(objective_entry.get(), materials_entry.get(), procedure_entry.get(), experiment_window)).pack(pady=10)

    def save_experiment(self, objective, materials, procedure, window):
        if objective and materials and procedure:
            experiment = Experiment(objective, materials, procedure)
            self.experiment_manager.add_experiment(experiment)
            self.experiment_manager.save_experiments()
            messagebox.showinfo("Success", "Experiment saved successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def view_experiments(self):
        experiments = self.experiment_manager.get_experiments()
        view_window = tk.Toplevel(self.root)
        view_window.title("View Experiments")

        for experiment in experiments:
            tk.Label(view_window, text=experiment.to_string()).pack()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()