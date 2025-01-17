import tkinter as tk
from tkinter import filedialog
from data_visualizer import DataVisualizer

class Main:
    def __init__(self):
        self.visualizer = DataVisualizer()
        self.root = tk.Tk()
        self.root.title("Data Visualization Tool")
        self.create_menu()
        self.root.mainloop()

    def create_menu(self) -> None:
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        visualize_menu = tk.Menu(menu)
        menu.add_cascade(label="Visualize", menu=visualize_menu)
        visualize_menu.add_command(label="Bar Chart", command=self.visualizer.create_bar_chart)
        visualize_menu.add_command(label="Line Graph", command=self.visualizer.create_line_graph)
        visualize_menu.add_command(label="Scatter Plot", command=self.visualizer.create_scatter_plot)
        visualize_menu.add_command(label="Pie Chart", command=self.visualizer.create_pie_chart)

        export_menu = tk.Menu(menu)
        menu.add_cascade(label="Export", menu=export_menu)
        export_menu.add_command(label="Export Visualization", command=self.export_visualization)

    def import_data(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.visualizer.import_data(file_path)

    def export_visualization(self) -> None:
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_name:
            self.visualizer.export_visualization(file_name)

if __name__ == "__main__":
    Main()