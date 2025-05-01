import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from image_processor import ImageProcessor
from sticker_creator import StickerCreator

class PhotoStickerMaker:
    def __init__(self, master):
        self.master = master
        self.master.title("Photo Sticker Maker")
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()
        
        self.create_widgets()
        
    def create_widgets(self):
        self.image_display = tk.Label(self.master, text="No Image Loaded", width=40, height=10)
        self.image_display.pack()

        self.import_button = tk.Button(self.master, text="Import Image", command=self.import_image)
        self.import_button.pack()

        self.crop_button = tk.Button(self.master, text="Crop Image", command=self.crop_image)
        self.crop_button.pack()

        self.resize_button = tk.Button(self.master, text="Resize Image", command=self.resize_image)
        self.resize_button.pack()

        self.effect_button = tk.Button(self.master, text="Apply Effect", command=self.apply_effect)
        self.effect_button.pack()

        self.shape_label = tk.Label(self.master, text="Choose Shape:")
        self.shape_label.pack()
        self.shape_var = tk.StringVar(self.master)
        self.shape_var.set("Circle")  # default value
        self.shape_menu = tk.OptionMenu(self.master, self.shape_var, "Circle", "Square", "Star")
        self.shape_menu.pack()

        self.text_entry = tk.Entry(self.master)
        self.text_entry.pack()

        self.color_button = tk.Button(self.master, text="Choose Text Color", command=self.choose_color)
        self.color_button.pack()

        self.save_button = tk.Button(self.master, text="Save Sticker", command=self.save_sticker)
        self.save_button.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.import_image(file_path)
            self.image_display.config(text="Image Loaded")

    def crop_image(self):
        # Placeholder for crop functionality
        pass

    def resize_image(self):
        # Placeholder for resize functionality
        pass

    def apply_effect(self):
        # Placeholder for effect functionality
        pass

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.sticker_creator.add_text(self.text_entry.get(), "Arial", color)

    def save_sticker(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.sticker_creator.save_sticker(file_path)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoStickerMaker(root)
    app.run()