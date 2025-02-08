import tkinter as tk
from day_planner import DayPlanner

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Day Planner")
        self.geometry("600x400")
        self.day_planner = DayPlanner()
        self.create_widgets()

    def create_widgets(self):
        self.task_list = tk.Listbox(self)
        self.task_list.pack(fill=tk.BOTH, expand=True)

        self.load_tasks()

        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT)

    def load_tasks(self):
        for task in self.day_planner.view_tasks():
            self.task_list.insert(tk.END, f"{task[0]} | Priority: {task[1]} | Category: {task[2]} | Time: {task[3]}")

    def add_task(self):
        # Placeholder for adding task logic
        pass

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            self.day_planner.delete(selected_task_index[0])
            self.task_list.delete(selected_task_index)

if __name__ == "__main__":
    app = Application()
    app.mainloop()