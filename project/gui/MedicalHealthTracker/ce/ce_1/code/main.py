from tkinter import Tk
from health_tracker import HealthTracker

class Main:
    def __init__(self):
        self.health_tracker = HealthTracker()

    def main(self):
        root = Tk()
        root.title("Medical Health Tracker")
        root.geometry("400x400")

        # Create buttons for each feature
        # Implement button commands to open respective windows

        root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()