import tkinter as tk
from tkinter import messagebox
from experiment_manager import ExperimentManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Science Experiment Planner")
        self.experiment_manager = ExperimentManager()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Experiment Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.master)
        self.title_entry.pack()

        self.objectives_label = tk.Label(self.master, text="Objectives:")
        self.objectives_label.pack()
        self.objectives_entry = tk.Text(self.master, height=5, width=40)
        self.objectives_entry.pack()

        self.materials_label = tk.Label(self.master, text="Materials:")
        self.materials_label.pack()
        self.materials_entry = tk.Text(self.master, height=5, width=40)
        self.materials_entry.pack()

        self.procedures_label = tk.Label(self.master, text="Procedures:")
        self.procedures_label.pack()
        self.procedures_entry = tk.Text(self.master, height=5, width=40)
        self.procedures_entry.pack()

        self.add_button = tk.Button(self.master, text="Add Experiment", command=self.add_experiment)
        self.add_button.pack()

        self.view_button = tk.Button(self.master, text="View Experiments", command=self.view_experiments)
        self.view_button.pack()

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.quit)
        self.exit_button.pack()

    def add_experiment(self):
        title = self.title_entry.get()
        objectives = self.objectives_entry.get("1.0", tk.END).strip()
        materials = self.materials_entry.get("1.0", tk.END).strip()
        procedures = self.procedures_entry.get("1.0", tk.END).strip()

        if title and objectives and materials and procedures:
            self.experiment_manager.add_experiment(title, objectives, materials, procedures)
            messagebox.showinfo("Success", "Experiment added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def view_experiments(self):
        experiments = self.experiment_manager.load_experiments()
        if experiments:
            messagebox.showinfo("Experiments", "\n".join(experiments))
        else:
            messagebox.showinfo("Experiments", "No experiments found.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.objectives_entry.delete("1.0", tk.END)
        self.materials_entry.delete("1.0", tk.END)
        self.procedures_entry.delete("1.0", tk.END)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()