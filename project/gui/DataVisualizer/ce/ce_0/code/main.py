import tkinter as tk
from tkinter import filedialog, messagebox
from data_handler import DataHandler
from visualization import Visualization

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer")
        
        self.data_handler = DataHandler()
        self.visualizer = Visualization()
        
        self.create_menu()
        
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Visualization", command=self.export_visualization)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        self.root.config(menu=menu_bar)
        
    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = self.data_handler.import_data(file_path)
            if data:
                self.visualizer.data = data
                messagebox.showinfo("Success", "Data imported successfully!")
            else:
                messagebox.showerror("Error", "Failed to import data.")
                
    def export_visualization(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.visualizer.export_image(file_path)
            messagebox.showinfo("Success", "Visualization exported successfully!")
        
    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()