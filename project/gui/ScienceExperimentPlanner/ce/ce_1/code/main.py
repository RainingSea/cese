import os
from tkinter import Tk, Menu, Frame, Label, Entry, Button, Text, END, Scrollbar, VERTICAL
from experiment import Experiment
from experiment_manager import ExperimentManager

class Main:
    def __init__(self) -> None:
        self.experiment_manager = ExperimentManager()
        self.root = Tk()
        self.root.title("Science Experiment Planner")
        self.create_menu()
        self.create_ui()
        self.root.mainloop()

    def create_menu(self) -> None:
        menu = Menu(self.root)
        self.root.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Experiment", command=self.save_experiment)
        file_menu.add_command(label="Load Experiment", command=self.load_experiment)

    def create_ui(self) -> None:
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        Label(self.frame, text="Title:").grid(row=0, column=0)
        self.title_entry = Entry(self.frame)
        self.title_entry.grid(row=0, column=1)

        Label(self.frame, text="Objectives:").grid(row=1, column=0)
        self.objectives_entry = Entry(self.frame)
        self.objectives_entry.grid(row=1, column=1)

        Label(self.frame, text="Materials:").grid(row=2, column=0)
        self.materials_entry = Entry(self.frame)
        self.materials_entry.grid(row=2, column=1)

        Label(self.frame, text="Procedures:").grid(row=3, column=0)
        self.procedures_entry = Entry(self.frame)
        self.procedures_entry.grid(row=3, column=1)

        Label(self.frame, text="Expected Results:").grid(row=4, column=0)
        self.expected_results_entry = Entry(self.frame)
        self.expected_results_entry.grid(row=4, column=1)

        Button(self.frame, text="Add Experiment", command=self.add_experiment).grid(row=5, columnspan=2)

        self.observation_text = Text(self.frame, height=10, width=50)
        self.observation_text.grid(row=6, columnspan=2)
        self.scrollbar = Scrollbar(self.frame, command=self.observation_text.yview, orient=VERTICAL)
        self.observation_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=2, sticky='ns')

    def add_experiment(self) -> None:
        experiment = Experiment(
            title=self.title_entry.get(),
            objectives=self.objectives_entry.get(),
            materials=self.materials_entry.get(),
            procedures=self.procedures_entry.get(),
            expected_results=self.expected_results_entry.get()
        )
        self.experiment_manager.add_experiment(experiment)
        self.clear_entries()

    def clear_entries(self) -> None:
        self.title_entry.delete(0, END)
        self.objectives_entry.delete(0, END)
        self.materials_entry.delete(0, END)
        self.procedures_entry.delete(0, END)
        self.expected_results_entry.delete(0, END)

    def save_experiment(self) -> None:
        if self.experiment_manager.experiments:
            for experiment in self.experiment_manager.experiments:
                self.experiment_manager.save_experiment(experiment)

    def load_experiment(self) -> None:
        title = self.title_entry.get()
        try:
            experiment = self.experiment_manager.load_experiment(title)
            self.title_entry.insert(0, experiment.title)
            self.objectives_entry.insert(0, experiment.objectives)
            self.materials_entry.insert(0, experiment.materials)
            self.procedures_entry.insert(0, experiment.procedures)
            self.expected_results_entry.insert(0, experiment.expected_results)
            self.observation_text.delete(1.0, END)
            for observation in experiment.observations:
                self.observation_text.insert(END, observation + '\n')
        except FileNotFoundError as e:
            print(e)

if __name__ == "__main__":
    Main()