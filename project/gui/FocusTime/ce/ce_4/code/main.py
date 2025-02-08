import tkinter as tk
from tkinter import messagebox
from timer import Timer

class FocusTimeApp:
    def __init__(self):
        self.work_duration = 25  # default work duration in minutes
        self.break_duration = 5   # default break duration in minutes
        self.timer = None
        
        self.load_settings()
        
        self.root = tk.Tk()
        self.root.title("FocusTime")
        
        self.work_label = tk.Label(self.root, text="Work Duration (min):")
        self.work_label.pack()
        
        self.work_entry = tk.Entry(self.root)
        self.work_entry.insert(0, str(self.work_duration))
        self.work_entry.pack()
        
        self.break_label = tk.Label(self.root, text="Break Duration (min):")
        self.break_label.pack()
        
        self.break_entry = tk.Entry(self.root)
        self.break_entry.insert(0, str(self.break_duration))
        self.break_entry.pack()
        
        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack()
        
        self.countdown_display = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.countdown_display.pack()

    def start_timer(self):
        work_time = int(self.work_entry.get()) * 60  # convert to seconds
        self.timer = Timer(work_time)
        self.timer.start()
        self.show_countdown(work_time)

    def show_countdown(self, remaining):
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            self.countdown_display.config(text=f"{mins:02}:{secs:02}")
            self.root.after(1000, self.show_countdown, remaining - 1)
        else:
            self.show_notification("Work interval completed!")
            self.start_break_timer()

    def start_break_timer(self):
        break_time = int(self.break_entry.get()) * 60  # convert to seconds
        self.timer = Timer(break_time)
        self.timer.start()
        self.show_countdown(break_time)

    def show_notification(self, message: str):
        messagebox.showinfo("Notification", message)

    def load_settings(self):
        try:
            with open('settings.txt', 'r') as file:
                settings = file.readlines()
                for line in settings:
                    key, value = line.strip().split('|')
                    if key == "work_duration":
                        self.work_duration = int(value)
                    elif key == "break_duration":
                        self.break_duration = int(value)
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        with open('settings.txt', 'w') as file:
            file.write(f"work_duration|{self.work_duration}\n")
            file.write(f"break_duration|{self.break_duration}\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FocusTimeApp()
    app.run()