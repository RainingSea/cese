import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Canvas, Scale, Button, HORIZONTAL
from PIL import Image as PILImage
from Image import Image as CustomImage

class ImageEnhancer:
    def __init__(self):
        self.image_path = None
        self.image = None

    def import_image(self, path: str) -> None:
        self.image_path = path
        self.image = CustomImage(path)

    def adjust_brightness(self, value: float) -> None:
        if self.image:
            enhancer = PILImageEnhance.Brightness(self.image.image)
            self.image.image = enhancer.enhance(value)

    def adjust_contrast(self, value: float) -> None:
        if self.image:
            enhancer = PILImageEnhance.Contrast(self.image.image)
            self.image.image = enhancer.enhance(value)

    def adjust_saturation(self, value: float) -> None:
        if self.image:
            enhancer = PILImageEnhance.Color(self.image.image)
            self.image.image = enhancer.enhance(value)

    def apply_filter(self, filter_name: str) -> None:
        if self.image:
            if filter_name == "BLUR":
                self.image.image = self.image.image.filter(PILImageFilter.BLUR)
            elif filter_name == "CONTOUR":
                self.image.image = self.image.image.filter(PILImageFilter.CONTOUR)

    def apply_effect(self, effect_name: str) -> None:
        pass  # Placeholder for future effects

    def crop_image(self, left: int, top: int, right: int, bottom: int) -> None:
        if self.image:
            self.image.image = self.image.image.crop((left, top, right, bottom))

    def resize_image(self, width: int, height: int) -> None:
        if self.image:
            self.image.image = self.image.image.resize((width, height))

    def save_image(self, path: str) -> None:
        if self.image:
            self.image.save(path)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Enhancer")
        self.geometry("800x600")
        self.image_enhancer = ImageEnhancer()
        self.create_widgets()

    def create_widgets(self):
        menu = Menu(self)
        self.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Image", command=self.import_image)

        self.canvas = Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brightness_scale = Scale(self, from_=0, to=2, resolution=0.1, orient=HORIZONTAL, label="Brightness", command=self.update_brightness)
        self.brightness_scale.pack()

        self.contrast_scale = Scale(self, from_=0, to=2, resolution=0.1, orient=HORIZONTAL, label="Contrast", command=self.update_contrast)
        self.contrast_scale.pack()

        self.saturation_scale = Scale(self, from_=0, to=2, resolution=0.1, orient=HORIZONTAL, label="Saturation", command=self.update_saturation)
        self.saturation_scale.pack()

        apply_button = Button(self, text="Apply Changes", command=self.apply_changes)
        apply_button.pack()

    def import_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image_enhancer.import_image(path)
            self.show_image()

    def show_image(self):
        self.image_enhancer.image.show()

    def update_brightness(self, value):
        self.image_enhancer.adjust_brightness(float(value))

    def update_contrast(self, value):
        self.image_enhancer.adjust_contrast(float(value))

    def update_saturation(self, value):
        self.image_enhancer.adjust_saturation(float(value))

    def apply_changes(self):
        # Logic to apply changes to the image and update the canvas
        pass  # Placeholder for future implementation

if __name__ == "__main__":
    app = Application()
    app.mainloop()