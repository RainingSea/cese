import tkinter as tk
from tkinter import filedialog, messagebox
from data_storage import DataAnalyzer

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Summarizer")
        self.data_analyzer = DataAnalyzer()

        self.import_button = tk.Button(root, text="Import Data", command=self.import_data)
        self.import_button.pack()

        self.summary_text = tk.Text(root, height=20, width=50)
        self.summary_text.pack()

    def import_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.data_analyzer.import_data(file_path)
                summary = self.data_analyzer.generate_summary()
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, summary)
            except Exception as e:
                messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()