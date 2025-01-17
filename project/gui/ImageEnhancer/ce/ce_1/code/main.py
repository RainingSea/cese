import tkinter as tk
from tkinter import filedialog, messagebox
from image_processor import ImageProcessor

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Enhancer")
        self.image_processor = ImageProcessor()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.load_image)

        self.enhancements_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Enhancements", menu=self.enhancements_menu)
        self.enhancements_menu.add_command(label="Adjust Brightness", command=self.adjust_brightness)
        self.enhancements_menu.add_command(label="Adjust Contrast", command=self.adjust_contrast)
        self.enhancements_menu.add_command(label="Adjust Saturation", command=self.adjust_saturation)

        self.save_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save Image", command=self.save_image)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.image_processor.image is not None:
            self.tk_image = ImageTk.PhotoImage(self.image_processor.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def adjust_brightness(self):
        value = self.get_adjustment_value("Brightness")
        if value is not None:
            self.image_processor.adjust_brightness(value)
            self.display_image()

    def adjust_contrast(self):
        value = self.get_adjustment_value("Contrast")
        if value is not None:
            self.image_processor.adjust_contrast(value)
            self.display_image()

    def adjust_saturation(self):
        value = self.get_adjustment_value("Saturation")
        if value is not None:
            self.image_processor.adjust_saturation(value)
            self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"),
                                                              ("JPEG files", "*.jpg"),
                                                              ("All files", "*.*")])
        if file_path:
            self.image_processor.save_image(file_path)

    def get_adjustment_value(self, adjustment_type):
        value = simpledialog.askfloat("Input", f"Enter {adjustment_type} value (0-2):", minvalue=0, maxvalue=2)
        return value

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()