import tkinter as tk
from tkinter import messagebox
import threading
import time

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuickTimer")
        
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)
        
        self.countdown_label = tk.Label(self.root, text="Time Left: 0 seconds")
        self.countdown_label.pack(pady=10)
        
        self.countdown = 0
        
        self.root.mainloop()
    
    def start_timer(self):
        try:
            self.countdown = int(self.time_entry.get())
            self.update_timer()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer.")
    
    def update_timer(self):
        if self.countdown > 0:
            self.countdown_label.config(text=f"Time Left: {self.countdown} seconds")
            self.countdown -= 1
            threading.Timer(1, self.update_timer).start()
        else:
            self.show_notification()
    
    def show_notification(self):
        messagebox.showinfo("Time's up!", "The timer has reached zero.")