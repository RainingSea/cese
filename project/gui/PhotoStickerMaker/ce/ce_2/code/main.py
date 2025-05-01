import os
from tkinter import Tk, Canvas, Button, Label, filedialog, StringVar, Entry, ColorVar, OptionMenu
from PIL import Image, ImageTk, ImageDraw, ImageFont

class Main:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()
        self.root = Tk()
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Sticker Creator")
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.import_button = Button(self.root, text="Import Photo", command=self.import_photo)
        self.import_button.pack()

        self.shape_var = StringVar(self.root)
        self.shape_var.set("Select Shape")
        self.shape_menu = OptionMenu(self.root, self.shape_var, "Circle", "Square", "Star")
        self.shape_menu.pack()

        self.size_var = StringVar(self.root)
        self.size_var.set("Select Size")
        self.size_menu = OptionMenu(self.root, self.size_var, "Small", "Medium", "Large")
        self.size_menu.pack()

        self.text_entry = Entry(self.root)
        self.text_entry.pack()

        self.color_var = ColorVar()
        self.color_button = Button(self.root, text="Choose Text Color", command=self.choose_color)
        self.color_button.pack()

        self.create_button = Button(self.root, text="Create Sticker", command=self.create_sticker)
        self.create_button.pack()

        self.save_button = Button(self.root, text="Save Sticker", command=self.save_sticker)
        self.save_button.pack()

    def import_photo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.show_image()

    def show_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def choose_color(self):
        # Placeholder for color chooser implementation
        pass

    def create_sticker(self):
        shape = self.shape_var.get()
        text = self.text_entry.get()
        color = self.color_var.get()
        self.sticker_creator.create_sticker(self.image, shape, text, color)

    def save_sticker(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.sticker_creator.save_sticker(self.image, filename)

class ImageProcessor:
    def crop(self, image: Image, dimensions: tuple) -> Image:
        return image.crop(dimensions)

    def resize(self, image: Image, size: tuple) -> Image:
        return image.resize(size)

    def apply_effect(self, image: Image, effect: str) -> Image:
        if effect == "grayscale":
            return image.convert("L")
        return image

class StickerCreator:
    def create_sticker(self, image: Image, shape: str, text: str, color: str) -> Image:
        shape_image = Shape().select_shape(shape)
        image.paste(shape_image, (0, 0), shape_image)
        return Text().add_text(image, text, "Arial", color)

    def save_sticker(self, image: Image, filename: str) -> None:
        image.save(filename, "PNG")

class Shape:
    def select_shape(self, shape_type: str) -> Image:
        shape_image = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(shape_image)
        if shape_type == "Circle":
            draw.ellipse((0, 0, 100, 100), fill=(255, 0, 0, 128))
        elif shape_type == "Square":
            draw.rectangle((0, 0, 100, 100), fill=(0, 255, 0, 128))
        elif shape_type == "Star":
            draw.polygon([(50, 0), (65, 35), (100, 35), (75, 57), (85, 90), (50, 70), (15, 90), (25, 57), (0, 35), (35, 35)], fill=(0, 0, 255, 128))
        return shape_image

class Text:
    def add_text(self, image: Image, text: str, font: str, color: str) -> Image:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((10, 10), text, fill=color, font=font)
        return image

if __name__ == "__main__":
    Main()