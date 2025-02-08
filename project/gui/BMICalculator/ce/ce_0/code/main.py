import tkinter as tk
from tkinter import messagebox
from bmi_calculator import BMI_Calculator

class Main:
    def __init__(self, master):
        self.master = master
        master.title("BMI Calculator")

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.pack()

        self.weight_entry = tk.Entry(master)
        self.weight_entry.pack()

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.pack()

        self.height_entry = tk.Entry(master)
        self.height_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def calculate_bmi(self):
        """Calculate BMI and display results."""
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi_calculator = BMI_Calculator(weight, height)

            result = f"BMI: {bmi_calculator.bmi}\n" \
                     f"Classification: {bmi_calculator.classify_bmi()}\n" \
                     f"Interpretation: {bmi_calculator.interpret_bmi()}\n" \
                     f"Recommendations: {bmi_calculator.recommendations()}"
            
            self.result_label.config(text=result)
            bmi_calculator.save_data()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()