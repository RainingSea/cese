import tkinter.messagebox

class Notification:
    def send_notification(self, message: str):
        tkinter.messagebox.showinfo("Notification", message)