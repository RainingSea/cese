import tkinter as tk
from tkinter import filedialog, messagebox
from statistics import mean, median, mode, StatisticsError
from collections import Counter

class DataAnalyzer:
    def __init__(self):
        self.numerical_data = []
        self.categorical_data = []

    def import_data(self, file_path: str) -> None:
        """Import data from a specified file path."""
        try:
            if file_path.endswith(".txt"):
                with open(file_path, 'r') as file:
                    data = file.readlines()
                    self.numerical_data = []
                    self.categorical_data = []

                    for line in data:
                        line = line.strip()
                        if any(char.isdigit() for char in line):
                            self.numerical_data.extend([float(x) for x in line.split(',') if x.strip().replace('.', '', 1).isdigit()])
                        elif '|' in line:
                            key, value = line.split('|')
                            self.categorical_data.append(key.strip())
                            self.categorical_data.append(value.strip())
                        else:
                            self.categorical_data.append(line)
            else:
                raise ValueError("Invalid file type. Only .txt files are supported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")

    def calculate_mean(self) -> float:
        """Calculate the mean of numerical data."""
        return mean(self.numerical_data) if self.numerical_data else 0.0

    def calculate_median(self) -> float:
        """Calculate the median of numerical data."""
        return median(self.numerical_data) if self.numerical_data else 0.0

    def calculate_mode(self) -> list:
        """Calculate the mode of numerical data."""
        if not self.numerical_data:
            return []
        try:
            return [mode(self.numerical_data)]
        except StatisticsError:
            return []

    def calculate_range(self) -> tuple:
        """Calculate the range of numerical data."""
        return (min(self.numerical_data), max(self.numerical_data)) if self.numerical_data else (None, None)

    def calculate_frequency(self) -> dict:
        """Calculate the frequency of categorical data."""
        return dict(Counter(self.categorical_data))

    def calculate_distribution(self) -> dict:
        """Calculate the distribution of categorical data."""
        total = len(self.categorical_data)
        frequency = self.calculate_frequency()
        return {key: value / total for key, value in frequency.items()} if total > 0 else {}

    def generate_summary(self) -> str:
        """Generate a summary of the analysis."""
        summary = []
        if self.numerical_data:
            summary.append(f"Mean: {self.calculate_mean()}")
            summary.append(f"Median: {self.calculate_median()}")
            summary.append(f"Mode: {self.calculate_mode()}")
            summary.append(f"Range: {self.calculate_range()}")
        if self.categorical_data:
            summary.append(f"Frequency: {self.calculate_frequency()}")
            summary.append(f"Distribution: {self.calculate_distribution()}")
        return "\n".join(summary)

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Summarizer")
        self.data_analyzer = DataAnalyzer()
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI widgets."""
        self.import_button = tk.Button(self.master, text="Import Numerical Data", command=self.import_numerical_data)
        self.import_button.pack()

        self.import_button_categorical = tk.Button(self.master, text="Import Categorical Data", command=self.import_categorical_data)
        self.import_button_categorical.pack()

        self.analyze_button = tk.Button(self.master, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.pack()

        self.result_text = tk.Text(self.master, height=15, width=50)
        self.result_text.pack()

    def import_numerical_data(self):
        """Import numerical data from a file."""
        file_path = filedialog.askopenfilename(title="Select Numerical Data File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.data_analyzer.import_data(file_path)

    def import_categorical_data(self):
        """Import categorical data from a file."""
        file_path = filedialog.askopenfilename(title="Select Categorical Data File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.data_analyzer.import_data(file_path)

    def analyze_data(self):
        """Analyze the imported data and display the summary."""
        summary = self.data_analyzer.generate_summary()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, summary)

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()