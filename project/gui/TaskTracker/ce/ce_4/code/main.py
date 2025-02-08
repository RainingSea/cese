from UI import UI
from TaskManager import TaskManager

if __name__ == "__main__":
    task_manager = TaskManager()
    ui = UI(task_manager)
    ui.window.mainloop()