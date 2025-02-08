import tkinter as tk
import time

class QuickTimer:
    def __init__(self):
        self.duration = 0
        self.window = tk.Tk()
        self.window.title("QuickTimer")
        
        self.duration_entry = tk.Entry(self.window)
        self.duration_entry.pack()
        
        self.start_button = tk.Button(self.window, text="Start Timer", command=self.start_timer)
        self.start_button.pack()
        
        self.timer_label = tk.Label(self.window, text="")
        self.timer_label.pack()
        
        self.load_settings()
        
    def start_timer(self):
        try:
            self.duration = int(self.duration_entry.get())
            self.update_timer()
        except ValueError:
            self.timer_label.config(text="Please enter a valid number.")
        
    def update_timer(self):
        if self.duration > 0:
            self.timer_label.config(text=str(self.duration))
            self.duration -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.notify_user()
            self.save_settings()
        
    def notify_user(self):
        tk.messagebox.showinfo("Time's Up!", "The timer has reached zero.")
        
    def load_settings(self):
        try:
            with open('timer_settings.txt', 'r') as file:
                last_duration = file.readline().strip()
                if last_duration:
                    self.duration_entry.insert(0, last_duration)
        except FileNotFoundError:
            with open('timer_settings.txt', 'w') as file:
                file.write("")

    def save_settings(self):
        with open('timer_settings.txt', 'w') as file:
            file.write(self.duration_entry.get())
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    timer_app = QuickTimer()
    timer_app.run()