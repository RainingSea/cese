import tkinter as tk
from tkinter import filedialog, messagebox
from image_processor import ImageProcessor
import os

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Enhancer")
        self.image_processor = ImageProcessor()
        self.last_directory = self.load_config()
        self.create_widgets()

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load Image", command=self.load_image)
        file_menu.add_command(label="Save Image", command=self.save_image)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        self.canvas = tk.Canvas(self.master, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brightness_slider = tk.Scale(self.master, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL, command=self.apply_adjustments)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.master, from_=-100, to=100, label="Contrast", orient=tk.HORIZONTAL, command=self.apply_adjustments)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.master, from_=-100, to=100, label="Saturation", orient=tk.HORIZONTAL, command=self.apply_adjustments)
        self.saturation_slider.pack()

        self.status_bar = tk.Label(self.master, text="Welcome to Image Enhancer", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_config(self):
        config_file = 'config.txt'
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                for line in file:
                    if line.startswith('last_used_directory='):
                        return line.split('=')[1].strip()
        return './'

    def save_config(self):
        with open('config.txt', 'w') as file:
            file.write(f"last_used_directory={self.last_directory}\n")
            file.write("user_preferences=default\n")

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir=self.last_directory, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.last_directory = os.path.dirname(file_path)
            self.save_config()
            self.image_processor.load_image(file_path)
            self.update_canvas()
            self.status_bar.config(text="Image Loaded")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", initialdir=self.last_directory, filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")])
        if file_path:
            self.image_processor.save_image(file_path)
            self.status_bar.config(text="Image Saved")

    def apply_adjustments(self, event=None):
        brightness = self.brightness_slider.get()
        contrast = self.contrast_slider.get()
        saturation = self.saturation_slider.get()
        self.image_processor.adjust_brightness(brightness)
        self.image_processor.adjust_contrast(contrast)
        self.image_processor.adjust_saturation(saturation)
        self.update_canvas()
        self.status_bar.config(text="Adjustments Applied")

    def update_canvas(self):
        self.canvas.delete("all")
        if self.image_processor.image:
            self.tk_image = self.image_processor.get_tk_image()
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()