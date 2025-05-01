import tkinter as tk
from tkinter import filedialog, messagebox
from data_handler import DataHandler

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Summarizer")
        self.data_handler = DataHandler()
        
        self.import_button = tk.Button(root, text="Import Data", command=self.import_data)
        self.import_button.pack(pady=10)

        self.variable_selection = tk.StringVar(root)
        self.variable_menu = tk.OptionMenu(root, self.variable_selection, *self.data_handler.get_variable_names())
        self.variable_menu.pack(pady=10)

        self.analyze_button = tk.Button(root, text="Analyze Data", command=self.analyze_data)
        self.analyze_button.pack(pady=10)

        self.summary_text = tk.Text(root, height=10, width=50)
        self.summary_text.pack(pady=10)

    def import_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.data_handler.import_data(file_path)
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def analyze_data(self):
        summary = self.data_handler.generate_summary()
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()