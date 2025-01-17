import tkinter as tk
from tkinter import messagebox
from ListManager import ListManager
from UI import UI

class MainApp:
    def __init__(self):
        self.list_manager = ListManager()
        self.ui = UI(self)

    def run(self):
        self.list_manager.load_lists()
        self.ui.create_main_window()
        tk.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()