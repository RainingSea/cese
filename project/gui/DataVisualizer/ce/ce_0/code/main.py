import tkinter as tk
from tkinter import filedialog
from data_visualizer import DataVisualizer

class Main:
    def __init__(self):
        self.data_visualizer = DataVisualizer()
        self.root = tk.Tk()
        self.root.title("Data Visualizer")
        self._create_menu()
        self._create_buttons()
        self.root.mainloop()

    def _create_menu(self):
        """Creates the menu bar for the application."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Visualization", command=self.export_visualization)
        menu_bar.add_cascade(label="File", menu=file_menu)

        visualization_menu = tk.Menu(menu_bar, tearoff=0)
        visualization_menu.add_command(label="Bar Chart", command=lambda: self.set_visualization_type('bar'))
        visualization_menu.add_command(label="Line Graph", command=lambda: self.set_visualization_type('line'))
        visualization_menu.add_command(label="Scatter Plot", command=lambda: self.set_visualization_type('scatter'))
        visualization_menu.add_command(label="Pie Chart", command=lambda: self.set_visualization_type('pie'))
        menu_bar.add_cascade(label="Visualizations", menu=visualization_menu)

    def _create_buttons(self):
        """Creates buttons for each visualization type."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Create Visualization", command=self.create_visualization).pack(side=tk.LEFT)

    def import_data(self):
        """Handles data import from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data_visualizer.import_data(file_path)

    def set_visualization_type(self, visualization_type: str):
        """Sets the visualization type for the data visualizer."""
        self.data_visualizer.visualization_type = visualization_type

    def create_visualization(self):
        """Creates the selected visualization."""
        self.data_visualizer.create_visualization()

    def export_visualization(self):
        """Exports the current visualization to a file."""
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_name:
            self.data_visualizer.export_visualization(file_name)

if __name__ == "__main__":
    Main()