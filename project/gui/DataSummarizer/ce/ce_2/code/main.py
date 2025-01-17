import tkinter as tk
from tkinter import filedialog, messagebox, Text
from data_analyzer import DataAnalyzer

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Summarizer")
        self.data_analyzer = DataAnalyzer()
        
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.import_button = tk.Button(self.root, text="Import CSV", command=self.import_data)
        self.import_button.pack()

        self.summary_button = tk.Button(self.root, text="Generate Summary", command=self.display_summary)
        self.summary_button.pack()

        self.text_area = Text(self.root, wrap='word', width=50, height=20)
        self.text_area.pack()

    def import_data(self):
        """Handle data import."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data_analyzer.import_data(file_path)
                messagebox.showinfo("Success", "Data imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {e}")

    def display_summary(self):
        """Display the summary of the data."""
        selected_vars = ['Column1', 'Column2']  # Example variable names
        try:
            summary = self.data_analyzer.generate_summary(selected_vars)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, summary)
            self.data_analyzer.save_summary("summary.txt", summary)
            messagebox.showinfo("Success", "Summary generated and saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate summary: {e}")

    def main(self):
        """Run the main loop of the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()