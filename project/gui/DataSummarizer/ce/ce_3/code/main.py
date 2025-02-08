import tkinter as tk
from tkinter import filedialog, messagebox
from data_analyzer import DataAnalyzer
from summary_display import SummaryDisplay

class Main:
    def __init__(self):
        self.data_analyzer = DataAnalyzer()
        self.summary_display = SummaryDisplay()
        self.root = tk.Tk()
        self.root.title("Data Summarizer")
        self.create_widgets()

    def create_widgets(self):
        """Creates the GUI widgets."""
        self.import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        self.import_button.pack(pady=10)

        self.analyze_button = tk.Button(self.root, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.pack(pady=10)

        self.text_area = tk.Text(self.root, height=20, width=50)
        self.text_area.pack(pady=10)

    def import_data(self):
        """Handles data import from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data_analyzer.import_data(file_path)
            messagebox.showinfo("Success", "Data imported successfully!")

    def analyze_data(self):
        """Handles data analysis and displays the summary."""
        numerical_vars = ['column1', 'column2']  # Example numerical columns
        categorical_vars = ['category1', 'category2']  # Example categorical columns
        
        numerical_summary = self.data_analyzer.compute_numerical_summary(numerical_vars)
        categorical_summary = self.data_analyzer.compute_categorical_summary(categorical_vars)

        self.text_area.delete(1.0, tk.END)  # Clear the text area
        self.summary_display.display_summary(numerical_summary)
        self.summary_display.display_summary(categorical_summary)

    def main(self):
        """Runs the main loop of the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()