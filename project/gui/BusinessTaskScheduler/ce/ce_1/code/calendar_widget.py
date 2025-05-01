import tkinter as tk
from tkcalendar import Calendar

class CalendarWidget:
    def __init__(self, root):
        self.root = root
        self.calendar = Calendar(root)
        self.calendar.pack()

    def display_calendar(self) -> None:
        self.calendar.pack()

    def select_date(self, date: str) -> None:
        selected_date = self.calendar.selection_get()
        print(f"Selected date: {selected_date}")