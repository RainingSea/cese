from TaskManager import TaskManager
from GUI import GUI

def main():
    task_manager = TaskManager()
    task_manager.load_tasks('tasks.txt')
    gui = GUI(task_manager)
    gui.run()
    task_manager.save_tasks('tasks.txt')

if __name__ == "__main__":
    main()