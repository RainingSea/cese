import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from image_enhancer import ImageEnhancer

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Enhancer")
        self.enhancer = None
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create and place all the widgets in the GUI."""
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.import_button = tk.Button(self.root, text="Import Image", command=self.import_image)
        self.import_button.pack()

        self.brightness_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Brightness", orient=tk.HORIZONTAL, command=self.adjust_brightness)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Contrast", orient=tk.HORIZONTAL, command=self.adjust_contrast)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Saturation", orient=tk.HORIZONTAL, command=self.adjust_saturation)
        self.saturation_slider.pack()

        self.filter_button = tk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack()

        self.crop_button = tk.Button(self.root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.resize_button = tk.Button(self.root, text="Resize Image", command=self.resize_image)
        self.resize_button.pack()

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_button.pack()

    def import_image(self) -> None:
        """Import an image file."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.enhancer = ImageEnhancer(file_path)
            self.display_image()

    def display_image(self) -> None:
        """Display the current image on the canvas."""
        img = ImageTk.PhotoImage(self.enhancer.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def adjust_brightness(self, value: float) -> None:
        """Adjust the brightness of the image."""
        if self.enhancer:
            self.enhancer.adjust_brightness(float(value))
            self.display_image()

    def adjust_contrast(self, value: float) -> None:
        """Adjust the contrast of the image."""
        if self.enhancer:
            self.enhancer.adjust_contrast(float(value))
            self.display_image()

    def adjust_saturation(self, value: float) -> None:
        """Adjust the saturation of the image."""
        if self.enhancer:
            self.enhancer.adjust_saturation(float(value))
            self.display_image()

    def apply_filter(self) -> None:
        """Apply a filter to the image."""
        filter_type = 'BLUR'  # This can be changed to any filter type
        if self.enhancer:
            self.enhancer.apply_filter(filter_type)
            self.display_image()

    def crop_image(self) -> None:
        """Crop the image (placeholder values)."""
        if self.enhancer:
            self.enhancer.crop_image(50, 50, 300, 300)  # Example crop box
            self.display_image()

    def resize_image(self) -> None:
        """Resize the image to a fixed size (placeholder values)."""
        if self.enhancer:
            self.enhancer.resize_image(200, 200)  # Example resize dimensions
            self.display_image()

    def save_image(self) -> None:
        """Save the enhanced image."""
        if self.enhancer:
            output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if output_path:
                self.enhancer.save_image(output_path)
                messagebox.showinfo("Image Saved", "Image has been saved successfully.")

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()