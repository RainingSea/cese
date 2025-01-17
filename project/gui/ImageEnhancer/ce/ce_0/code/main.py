import tkinter as tk
from tkinter import filedialog, messagebox
from image_processor import ImageProcessor

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancer")
        self.image_processor = ImageProcessor()
        
        self.create_widgets()

    def create_widgets(self):
        # Menu Bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Canvas for displaying image
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        # Sliders for adjustments
        self.brightness_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness", command=self.adjust_brightness)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Contrast", command=self.adjust_contrast)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Saturation", command=self.adjust_saturation)
        self.saturation_slider.pack()

        # Buttons for filters and effects
        filter_frame = tk.Frame(self.root)
        filter_frame.pack()

        tk.Button(filter_frame, text="Apply Blur", command=lambda: self.apply_filter("BLUR")).pack(side=tk.LEFT)
        tk.Button(filter_frame, text="Apply Grayscale", command=lambda: self.apply_effect("GRAYSCALE")).pack(side=tk.LEFT)

        # Save Button
        tk.Button(self.root, text="Save", command=self.save_image).pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.image_processor.image:
            self.image_processor.image.show()

    def adjust_brightness(self, value):
        self.image_processor.adjust_brightness(float(value))

    def adjust_contrast(self, value):
        self.image_processor.adjust_contrast(float(value))

    def adjust_saturation(self, value):
        self.image_processor.adjust_saturation(float(value))

    def apply_filter(self, filter_type):
        self.image_processor.apply_filter(filter_type)
        self.display_image()

    def apply_effect(self, effect_type):
        self.image_processor.apply_effect(effect_type)
        self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.image_processor.save_image(file_path)
            self.image_processor.save_history('image_history.txt')

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()