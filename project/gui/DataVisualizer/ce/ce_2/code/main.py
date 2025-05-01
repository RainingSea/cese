import tkinter as tk
from tkinter import filedialog, messagebox
from data_visualizer import DataVisualizer

class Main:
    def __init__(self):
        self.visualizer = DataVisualizer()
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Data Visualization App")

        import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        import_button.pack()

        self.visualization_type = tk.StringVar(self.root)
        self.visualization_type.set("Select Visualization Type")
        visualization_menu = tk.OptionMenu(self.root, self.visualization_type, "Bar Chart", "Line Graph", "Scatter Plot", "Pie Chart")
        visualization_menu.pack()

        customize_button = tk.Button(self.root, text="Customize Visualization", command=self.customize_visualization)
        customize_button.pack()

        export_button = tk.Button(self.root, text="Export Visualization", command=self.export_visualization)
        export_button.pack()

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.root.mainloop()

    def import_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.visualizer.import_data(file_path)
                messagebox.showinfo("Success", "Data imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def customize_visualization(self):
        colors = ["#FF0000", "#00FF00", "#0000FF"]  # Example colors
        labels = ["Label1", "Label2", "Label3"]  # Example labels
        title = "Sample Visualization Title"
        self.visualizer.customize_visualization(colors, labels, title)

    def export_visualization(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            try:
                self.visualizer.export_visualization(file_path)
                messagebox.showinfo("Success", "Visualization exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main = Main()