import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from image_processor import ImageProcessor

class MainApp:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.root = tk.Tk()
        self.root.title("Image Editor")
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.create_menu()
        self.create_sliders()
        self.root.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Image", command=self.import_image)
        file_menu.add_command(label="Save Image", command=self.save_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Adjust Brightness", command=self.adjust_brightness)
        edit_menu.add_command(label="Adjust Contrast", command=self.adjust_contrast)
        edit_menu.add_command(label="Adjust Saturation", command=self.adjust_saturation)
        edit_menu.add_command(label="Apply Filter", command=self.apply_filter)
        edit_menu.add_command(label="Apply Effect", command=self.apply_effect)
        edit_menu.add_command(label="Crop Image", command=self.crop_image)
        edit_menu.add_command(label="Resize Image", command=self.resize_image)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def create_sliders(self):
        self.brightness_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness")
        self.brightness_slider.pack()
        self.contrast_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Contrast")
        self.contrast_slider.pack()
        self.saturation_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, label="Saturation")
        self.saturation_slider.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.image_processor.image:
            self.tk_image = ImageTk.PhotoImage(self.image_processor.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.image_processor.save_image(file_path)

    def adjust_brightness(self):
        value = self.brightness_slider.get()
        self.image_processor.adjust_brightness(value)
        self.display_image()

    def adjust_contrast(self):
        value = self.contrast_slider.get()
        self.image_processor.adjust_contrast(value)
        self.display_image()

    def adjust_saturation(self):
        value = self.saturation_slider.get()
        self.image_processor.adjust_saturation(value)
        self.display_image()

    def apply_filter(self):
        filter_type = simpledialog.askstring("Filter Type", "Enter filter type (BLUR, CONTOUR, DETAIL):")
        if filter_type:
            self.image_processor.apply_filter(filter_type.upper())
            self.display_image()

    def apply_effect(self):
        effect_type = simpledialog.askstring("Effect Type", "Enter effect type (SHARPEN):")
        if effect_type:
            self.image_processor.apply_effect(effect_type.upper())
            self.display_image()

    def crop_image(self):
        left = simpledialog.askinteger("Crop", "Enter left coordinate:")
        upper = simpledialog.askinteger("Crop", "Enter upper coordinate:")
        right = simpledialog.askinteger("Crop", "Enter right coordinate:")
        lower = simpledialog.askinteger("Crop", "Enter lower coordinate:")
        if left is not None and upper is not None and right is not None and lower is not None:
            self.image_processor.crop_image(left, upper, right, lower)
            self.display_image()

    def resize_image(self):
        width = simpledialog.askinteger("Resize", "Enter new width:")
        height = simpledialog.askinteger("Resize", "Enter new height:")
        if width is not None and height is not None:
            self.image_processor.resize_image(width, height)
            self.display_image()