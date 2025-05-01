import tkinter as tk
from tkinter import filedialog, messagebox
from data_analyzer import DataAnalyzer

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Analyzer")
        self.data_analyzer = DataAnalyzer()

        self.import_button = tk.Button(master, text="Import Data", command=self.import_data)
        self.import_button.pack()

        self.variable_selection = tk.StringVar(master)
        self.variable_dropdown = tk.OptionMenu(master, self.variable_selection, "Select Variable")
        self.variable_dropdown.pack()

        self.summary_label = tk.Label(master, text="")
        self.summary_label.pack()

        self.analyze_button = tk.Button(master, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.pack()

    def import_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.data_analyzer.import_data(file_path)
                messagebox.showinfo("Success", "Data imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def analyze_data(self):
        summary = self.data_analyzer.generate_summary()
        self.summary_label.config(text=summary)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()