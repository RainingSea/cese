import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu, Text
from data_analyzer import DataAnalyzer

class Main:
    def __init__(self):
        self.data_analyzer = DataAnalyzer()
        self.root = tk.Tk()
        self.root.title("Data Analysis Application")
        
        self.variable_selection = StringVar(self.root)
        self.variable_selection.set("Select Variable")  # default value

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        import_button = tk.Button(self.root, text="Import Data", command=self.import_data)
        import_button.pack()

        self.variable_menu = OptionMenu(self.root, self.variable_selection, [])
        self.variable_menu.pack()

        analyze_button = tk.Button(self.root, text="Analyze", command=self.choose_variables)
        analyze_button.pack()

        self.summary_text = Text(self.root, height=15, width=50)
        self.summary_text.pack()

        self.root.mainloop()

    def import_data(self) -> None:
        """Import data from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data_analyzer.load_data(file_path)
            self.update_variable_menu()
            messagebox.showinfo("Success", "Data imported successfully!")

    def update_variable_menu(self) -> None:
        """Update the variable selection dropdown with the loaded data columns."""
        columns = self.data_analyzer.data.columns.tolist()
        self.variable_menu['menu'].delete(0, 'end')
        for col in columns:
            self.variable_menu['menu'].add_command(label=col, command=tk._setit(self.variable_selection, col))

    def choose_variables(self) -> None:
        """Choose a variable and display its analysis."""
        variable = self.variable_selection.get()
        if variable == "Select Variable":
            messagebox.showwarning("Warning", "Please select a variable.")
            return
        
        mean = self.data_analyzer.calculate_mean(variable)
        median = self.data_analyzer.calculate_median(variable)
        mode = self.data_analyzer.calculate_mode(variable)
        data_range = self.data_analyzer.calculate_range(variable)

        summary = f"Mean: {mean}\nMedian: {median}\nMode: {mode}\nRange: {data_range}"
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

if __name__ == "__main__":
    main = Main()