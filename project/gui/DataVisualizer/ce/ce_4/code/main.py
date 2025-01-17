import tkinter as tk
from tkinter import filedialog
from data_visualizer import DataVisualizer

class Main:
    def __init__(self):
        self.visualizer = DataVisualizer()
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        """Sets up the main UI components."""
        self.root.title("Data Visualization Tool")

        import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        import_button.pack()

        visualize_button = tk.Button(self.root, text="Visualize Data", command=self.visualize_data)
        visualize_button.pack()

        self.root.mainloop()

    def import_data(self):
        """Handles the import data action."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.visualizer.import_data(file_path)

    def visualize_data(self):
        """Handles the visualization action."""
        visualization_type = 'bar'  # Example visualization type
        self.visualizer.create_visualization(visualization_type)

if __name__ == "__main__":
    main = Main()