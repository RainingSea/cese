import tkinter as tk
from tkinter import messagebox, filedialog
from data_handler import DataHandler
from visualizer import Visualizer

class Main:
    def __init__(self):
        self.data_handler = DataHandler()
        self.visualizer = Visualizer()

    def main(self):
        self.root = tk.Tk()
        self.root.title("Data Visualizer")
        self.create_menu()
        self.root.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Visualization", command=self.export_visualization)
        menu_bar.add_cascade(label="File", menu=file_menu)

        visualize_menu = tk.Menu(menu_bar, tearoff=0)
        visualize_menu.add_command(label="Bar Chart", command=self.visualize_bar_chart)
        visualize_menu.add_command(label="Line Graph", command=self.visualize_line_graph)
        visualize_menu.add_command(label="Scatter Plot", command=self.visualize_scatter_plot)
        visualize_menu.add_command(label="Pie Chart", command=self.visualize_pie_chart)
        menu_bar.add_cascade(label="Visualize", menu=visualize_menu)

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            if self.data_handler.import_data(file_path):
                messagebox.showinfo("Success", "Data imported successfully.")
                self.visualizer.set_data(self.data_handler.dataFrame)
            else:
                messagebox.showerror("Error", "Failed to import data.")

    def export_visualization(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_name:
            self.visualizer.export_visualization(file_name)
            messagebox.showinfo("Success", "Visualization exported successfully.")

    def visualize_bar_chart(self):
        self.visualizer.create_bar_chart()

    def visualize_line_graph(self):
        self.visualizer.create_line_graph()

    def visualize_scatter_plot(self):
        self.visualizer.create_scatter_plot()

    def visualize_pie_chart(self):
        self.visualizer.create_pie_chart()

if __name__ == "__main__":
    app = Main()
    app.main()