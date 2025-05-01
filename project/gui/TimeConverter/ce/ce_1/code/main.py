import tkinter as tk
from tkinter import ttk, messagebox
from time_converter import TimeConverter

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Converter")
        self.time_converter = TimeConverter()
        
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Time input
        self.time_label = tk.Label(self.root, text="Enter time (HH:MM):")
        self.time_label.grid(row=0, column=0)

        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(row=0, column=1)

        # Source timezone
        self.source_tz_label = tk.Label(self.root, text="Source Timezone:")
        self.source_tz_label.grid(row=1, column=0)

        self.source_tz = ttk.Combobox(self.root, values=self.time_converter.get_timezones())
        self.source_tz.grid(row=1, column=1)

        # Target timezone
        self.target_tz_label = tk.Label(self.root, text="Target Timezone:")
        self.target_tz_label.grid(row=2, column=0)

        self.target_tz = ttk.Combobox(self.root, values=self.time_converter.get_timezones())
        self.target_tz.grid(row=2, column=1)

        # Time format
        self.format_var = tk.StringVar(value="24-hour")
        self.format_12h = tk.Radiobutton(self.root, text="12-hour", variable=self.format_var, value="12-hour")
        self.format_12h.grid(row=3, column=0)
        self.format_24h = tk.Radiobutton(self.root, text="24-hour", variable=self.format_var, value="24-hour")
        self.format_24h.grid(row=3, column=1)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_time)
        self.convert_button.grid(row=4, column=0, columnspan=2)

        # Converted time display
        self.converted_time_label = tk.Label(self.root, text="Converted Time:")
        self.converted_time_label.grid(row=5, column=0)

        self.converted_time_display = tk.Label(self.root, text="")
        self.converted_time_display.grid(row=5, column=1)

        # History display
        self.history_label = tk.Label(self.root, text="Conversion History:")
        self.history_label.grid(row=6, column=0)

        self.history_text = tk.Text(self.root, height=10, width=50)
        self.history_text.grid(row=7, column=0, columnspan=2)

        # Clear history button
        self.clear_history_button = tk.Button(self.root, text="Clear History", command=self.clear_history)
        self.clear_history_button.grid(row=8, column=0, columnspan=2)

    def convert_time(self):
        source_time = self.time_entry.get()
        source_tz = self.source_tz.get()
        target_tz = self.target_tz.get()
        time_format = self.format_var.get()

        try:
            converted_time = self.time_converter.convert_time(source_time, source_tz, target_tz, time_format)
            self.converted_time_display.config(text=converted_time)
            self.time_converter.save_conversion(source_time, source_tz, target_tz, converted_time, time_format)
            self.load_history()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_history(self):
        history = self.time_converter.load_history()
        self.history_text.delete(1.0, tk.END)
        for entry in history:
            self.history_text.insert(tk.END, entry + "\n")

    def clear_history(self):
        self.time_converter.clear_history()
        self.load_history()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()