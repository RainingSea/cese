import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import json
import os

class Main:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.last_directory = self.load_config().get("last_directory", "")
        self.setup_ui()

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as config_file:
                return json.load(config_file)
        return {}

    def save_config(self):
        config_data = {"last_directory": self.last_directory}
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file)

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Image Processor")

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.brightness_slider = tk.Scale(self.root, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL, command=self.adjust_brightness)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.root, from_=-100, to=100, label="Contrast", orient=tk.HORIZONTAL, command=self.adjust_contrast)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.root, from_=-100, to=100, label="Saturation", orient=tk.HORIZONTAL, command=self.adjust_saturation)
        self.saturation_slider.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir=self.last_directory, title="Select Image",
                                                filetypes=(("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")))
        if file_path:
            self.last_directory = os.path.dirname(file_path)
            self.save_config()
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.image_processor.image:
            self.tk_image = ImageTk.PhotoImage(self.image_processor.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def adjust_brightness(self, value):
        self.image_processor.adjust_brightness(int(value))
        self.display_image()

    def adjust_contrast(self, value):
        self.image_processor.adjust_contrast(int(value))
        self.display_image()

    def adjust_saturation(self, value):
        self.image_processor.adjust_saturation(int(value))
        self.display_image()

    def on_closing(self):
        self.save_config()
        self.root.destroy()

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, file_path: str):
        self.image = Image.open(file_path)

    def adjust_brightness(self, value: float):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def adjust_contrast(self, value: float):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def adjust_saturation(self, value: float):
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(1 + value / 100)

    def apply_filter(self, filter_type: str):
        if filter_type == "BLUR":
            self.image = self.image.filter(ImageFilter.BLUR)
        elif filter_type == "CONTOUR":
            self.image = self.image.filter(ImageFilter.CONTOUR)

    def apply_effect(self, effect_type: str):
        if effect_type == "SHARPEN":
            self.image = self.image.filter(ImageFilter.SHARPEN)

    def crop_image(self, x: int, y: int, width: int, height: int):
        self.image = self.image.crop((x, y, x + width, y + height))

    def resize_image(self, new_width: int, new_height: int):
        self.image = self.image.resize((new_width, new_height))

    def save_image(self, file_path: str):
        self.image.save(file_path)