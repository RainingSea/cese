import tkinter as tk
from tkinter import filedialog, Text, messagebox
from data_analyzer import DataAnalyzer

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Summarizer")
        self.data_analyzer = DataAnalyzer()

        self.import_button = tk.Button(master, text="Import CSV", command=self.import_data)
        self.import_button.pack()

        self.summary_button = tk.Button(master, text="Generate Summary", command=self.generate_summary)
        self.summary_button.pack()

        self.text_area = Text(master, height=15, width=50)
        self.text_area.pack()

    def import_data(self):
        """Import data from a CSV file and display a message."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data_analyzer.import_data(file_path)
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {e}")

    def generate_summary(self):
        """Generate summary of the data and display it in the text area."""
        if self.data_analyzer.data.empty:
            messagebox.showwarning("Warning", "No data imported!")
            return
        
        columns = self.data_analyzer.data.columns.tolist()
        summary = self.data_analyzer.generate_summary(columns)
        self.text_area.delete(1.0, tk.END)  # Clear previous text

        for column, stats in summary.items():
            self.text_area.insert(tk.END, f"Summary for {column}:\n")
            for stat_name, value in stats.items():
                self.text_area.insert(tk.END, f"{stat_name}: {value}\n")
            self.text_area.insert(tk.END, "\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()