import tkinter as tk
from tkinter import filedialog
from data_visualizer import DataVisualizer

class Main:
    def __init__(self):
        self.visualizer = DataVisualizer()
        self.root = tk.Tk()
        self.root.title("Data Visualization Tool")
        self.create_widgets()

    def create_widgets(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Visualization", command=self.export_visualization)

        self.visualization_type_var = tk.StringVar(value="bar")
        visualization_menu = tk.Menu(menu)
        menu.add_cascade(label="Visualizations", menu=visualization_menu)
        visualization_menu.add_radiobutton(label="Bar Chart", variable=self.visualization_type_var, value="bar")
        visualization_menu.add_radiobutton(label="Line Chart", variable=self.visualization_type_var, value="line")
        visualization_menu.add_radiobutton(label="Scatter Plot", variable=self.visualization_type_var, value="scatter")

        self.customization_frame = tk.Frame(self.root)
        self.customization_frame.pack()

        tk.Label(self.customization_frame, text="Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.customization_frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.customization_frame, text="X-axis Label:").grid(row=1, column=0)
        self.xlabel_entry = tk.Entry(self.customization_frame)
        self.xlabel_entry.grid(row=1, column=1)

        tk.Label(self.customization_frame, text="Y-axis Label:").grid(row=2, column=0)
        self.ylabel_entry = tk.Entry(self.customization_frame)
        self.ylabel_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Create Visualization", command=self.create_visualization).pack()

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.visualizer.import_data(file_path)

    def create_visualization(self):
        self.visualizer.visualization_type = self.visualization_type_var.get()
        options = {
            'title': self.title_entry.get(),
            'xlabel': self.xlabel_entry.get(),
            'ylabel': self.ylabel_entry.get()
        }
        self.visualizer.customize_visualization(options)
        self.visualizer.create_visualization()

    def export_visualization(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            self.visualizer.export_visualization(output_path)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()