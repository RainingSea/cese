import tkinter as tk
from tkinter import messagebox
from UserSettings import UserSettings
from PomodoroTimer import PomodoroTimer

class MainApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pomodoro Timer")
        self.settings = UserSettings('settings.txt')
        self.user_settings = self.settings.load_settings()
        self.timer = PomodoroTimer(self.user_settings['work_duration'], self.user_settings['break_duration'])

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.work_label = tk.Label(self.window, text="Work Duration (min):")
        self.work_label.pack()

        self.work_entry = tk.Entry(self.window)
        self.work_entry.insert(0, str(self.user_settings['work_duration']))
        self.work_entry.pack()

        self.break_label = tk.Label(self.window, text="Break Duration (min):")
        self.break_label.pack()

        self.break_entry = tk.Entry(self.window)
        self.break_entry.insert(0, str(self.user_settings['break_duration']))
        self.break_entry.pack()

        self.start_button = tk.Button(self.window, text="Start", command=self.start_button_clicked)
        self.start_button.pack()

        self.timer_display = tk.Label(self.window, text="")
        self.timer_display.pack()

    def start_button_clicked(self):
        try:
            work_duration = int(self.work_entry.get())
            break_duration = int(self.break_entry.get())
            self.settings.save_settings(work_duration, break_duration)
            self.timer = PomodoroTimer(work_duration, break_duration)
            self.timer.start_timer(is_break=False)
            self.update_display()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers for durations.")

    def update_display(self):
        remaining_time = self.timer.update_timer()
        minutes, seconds = divmod(remaining_time, 60)
        self.timer_display.config(text=f"{minutes:02}:{seconds:02}")
        if self.timer.is_running:
            self.window.after(1000, self.update_display)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()