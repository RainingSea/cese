import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from image_enhancer import ImageEnhancer

class GUI:
    def __init__(self):
        self.image_enhancer = ImageEnhancer()
        self.root = tk.Tk()
        self.create_main_window()
        self.create_canvas()
        self.create_sliders()
        self.create_buttons()

    def create_main_window(self) -> None:
        self.root.title("Image Enhancer")
        self.root.geometry("800x600")

    def create_canvas(self) -> None:
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

    def create_sliders(self) -> None:
        self.brightness_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Brightness", orient="horizontal", command=self.update_brightness)
        self.brightness_slider.pack()
        self.contrast_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Contrast", orient="horizontal", command=self.update_contrast)
        self.contrast_slider.pack()
        self.saturation_slider = tk.Scale(self.root, from_=0, to=2, resolution=0.1, label="Saturation", orient="horizontal", command=self.update_saturation)
        self.saturation_slider.pack()

    def create_buttons(self) -> None:
        import_button = tk.Button(self.root, text="Import Image", command=self.import_image)
        import_button.pack()
        save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        save_button.pack()
        blur_button = tk.Button(self.root, text="Apply Blur", command=lambda: self.apply_filter("BLUR"))
        blur_button.pack()
        contour_button = tk.Button(self.root, text="Apply Contour", command=lambda: self.apply_filter("CONTOUR"))
        contour_button.pack()
        detail_button = tk.Button(self.root, text="Apply Detail", command=lambda: self.apply_filter("DETAIL"))
        detail_button.pack()

    def update_brightness(self, value: float) -> None:
        self.image_enhancer.adjust_brightness(float(value))
        self.update_image_display()

    def update_contrast(self, value: float) -> None:
        self.image_enhancer.adjust_contrast(float(value))
        self.update_image_display()

    def update_saturation(self, value: float) -> None:
        self.image_enhancer.adjust_saturation(float(value))
        self.update_image_display()

    def import_image(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_enhancer.import_image(file_path)
            self.update_image_display()

    def apply_filter(self, filter_type: str) -> None:
        self.image_enhancer.apply_filter(filter_type)
        self.update_image_display()

    def save_image(self) -> None:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            self.image_enhancer.save_image(save_path)
            messagebox.showinfo("Image Saved", "Image has been saved successfully.")

    def update_image_display(self) -> None:
        if self.image_enhancer.edited_image:
            self.tk_image = ImageTk.PhotoImage(self.image_enhancer.edited_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.image = self.tk_image

    def run(self) -> None:
        self.root.mainloop()