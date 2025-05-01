import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import logging

class Main:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.root = tk.Tk()
        self.root.title("Image Editor")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Image", command=self.import_image)

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        brightness_button = tk.Button(self.root, text="Adjust Brightness", command=self.adjust_brightness)
        brightness_button.pack()

        contrast_button = tk.Button(self.root, text="Adjust Contrast", command=self.adjust_contrast)
        contrast_button.pack()

        saturation_button = tk.Button(self.root, text="Adjust Saturation", command=self.adjust_saturation)
        saturation_button.pack()

        filter_button = tk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        filter_button.pack()

        crop_button = tk.Button(self.root, text="Crop", command=self.crop_image)
        crop_button.pack()

        resize_button = tk.Button(self.root, text="Resize", command=self.resize_image)
        resize_button.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.import_image(file_path)
            self.display_image()

    def display_image(self):
        img = Image.open(self.image_processor.image)
        img.thumbnail((800, 600))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def adjust_brightness(self):
        value = self.get_adjustment_value("Brightness")
        self.image_processor.adjust_brightness(value)
        self.display_image()

    def adjust_contrast(self):
        value = self.get_adjustment_value("Contrast")
        self.image_processor.adjust_contrast(value)
        self.display_image()

    def adjust_saturation(self):
        value = self.get_adjustment_value("Saturation")
        self.image_processor.adjust_saturation(value)
        self.display_image()

    def apply_filter(self):
        filter_type = self.get_filter_type()
        self.image_processor.apply_filter(filter_type)
        self.display_image()

    def crop_image(self):
        x, y, width, height = self.get_crop_dimensions()
        self.image_processor.crop(x, y, width, height)
        self.display_image()

    def resize_image(self):
        width, height = self.get_resize_dimensions()
        self.image_processor.resize(width, height)
        self.display_image()

    def get_adjustment_value(self, adjustment_type):
        value = simpledialog.askinteger("Input", f"Enter {adjustment_type} value:")
        return value if value is not None else 0

    def get_filter_type(self):
        return simpledialog.askstring("Input", "Enter filter type:")

    def get_crop_dimensions(self):
        x = simpledialog.askinteger("Input", "Enter x coordinate:")
        y = simpledialog.askinteger("Input", "Enter y coordinate:")
        width = simpledialog.askinteger("Input", "Enter width:")
        height = simpledialog.askinteger("Input", "Enter height:")
        return x, y, width, height

    def get_resize_dimensions(self):
        width = simpledialog.askinteger("Input", "Enter new width:")
        height = simpledialog.askinteger("Input", "Enter new height:")
        return width, height

if __name__ == "__main__":
    Main()