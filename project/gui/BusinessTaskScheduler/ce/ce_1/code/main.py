import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from calendar_widget import CalendarWidget

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Task Scheduler")
        self.task_manager = TaskManager()
        self.task_manager.load_data()
        self.create_widgets()

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        task_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="Tasks", menu=task_menu)
        task_menu.add_command(label="Create Task", command=self.create_task)
        task_menu.add_command(label="Assign Task", command=self.assign_task)

        self.task_list_display = tk.Listbox(self.root)
        self.task_list_display.pack(fill=tk.BOTH, expand=True)

        self.update_task_list()

    def create_task(self):
        # Implementation for creating a task
        pass

    def assign_task(self):
        # Implementation for assigning a task
        pass

    def update_task_list(self):
        self.task_list_display.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_list_display.insert(tk.END, task)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()