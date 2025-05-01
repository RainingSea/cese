import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from visualization import Visualization
from data_handler import DataHandler

class DataVisualizer:
    def __init__(self, master):
        self.master = master
        self.data_handler = DataHandler()
        self.visualizations = Visualization()
        self.data = None
        
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Data Visualizer")
        
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        menubar.add_cascade(label="File", menu=file_menu)

        visualization_menu = tk.Menu(menubar, tearoff=0)
        visualization_menu.add_command(label="Bar Chart", command=lambda: self.create_visualization("bar"))
        visualization_menu.add_command(label="Line Graph", command=lambda: self.create_visualization("line"))
        visualization_menu.add_command(label="Scatter Plot", command=lambda: self.create_visualization("scatter"))
        visualization_menu.add_command(label="Pie Chart", command=lambda: self.create_visualization("pie"))
        menubar.add_cascade(label="Visualizations", menu=visualization_menu)

        export_menu = tk.Menu(menubar, tearoff=0)
        export_menu.add_command(label="Export Visualization", command=self.export_visualization)
        menubar.add_cascade(label="Export", menu=export_menu)

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = self.data_handler.load_data(file_path)
            messagebox.showinfo("Success", "Data imported successfully!")

    def create_visualization(self, type):
        if self.data is not None:
            if type == "bar":
                self.visualizations.draw_bar_chart(self.data)
            elif type == "line":
                self.visualizations.draw_line_graph(self.data)
            elif type == "scatter":
                self.visualizations.draw_scatter_plot(self.data)
            elif type == "pie":
                self.visualizations.draw_pie_chart(self.data)
        else:
            messagebox.showwarning("Warning", "No data imported!")

    def export_visualization(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            # Assume the last created visualization is stored in self.visualizations
            self.visualizations.export(file_path)
            messagebox.showinfo("Success", "Visualization exported successfully!")

def main():
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()