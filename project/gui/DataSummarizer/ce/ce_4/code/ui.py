import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from data_analyzer import DataAnalyzer

class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Summarizer")
        self.data_analyzer = DataAnalyzer()
        self.file_path = None
        self.selected_columns = []

        self.create_main_window()

    def create_main_window(self):
        """Creates the main window and its components."""
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Import Data', command=self.select_file)

        self.analyze_button = tk.Button(self.master, text='Analyze Data', command=self.analyze_data)
        self.analyze_button.pack()

        self.text_area = tk.Text(self.master)
        self.text_area.pack()

    def select_file(self):
        """Opens a file dialog to select a CSV file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.load_data()

    def load_data(self):
        """Loads data from the selected CSV file and creates checkboxes for columns."""
        data = self.data_analyzer.import_data(self.file_path)
        self.selected_columns = []

        for column in data.columns:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.master, text=column, variable=var)
            checkbox.var = var
            checkbox.pack()
            self.selected_columns.append((column, var))

    def analyze_data(self):
        """Triggers the analysis of the selected data columns."""
        selected = [col for col, var in self.selected_columns if var.get() == 1]
        if not selected:
            messagebox.showwarning("Warning", "No columns selected for analysis.")
            return

        data = self.data_analyzer.import_data(self.file_path)
        summary = self.data_analyzer.calculate_statistics(data, selected)
        self.show_summary(summary)

    def show_summary(self, summary: dict):
        """Displays the summary of the analysis in the text area."""
        self.text_area.delete(1.0, tk.END)
        for column, stats in summary.items():
            self.text_area.insert(tk.END, f"Summary for {column}:\n{stats}\n\n")