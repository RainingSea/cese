import os
from tkinter import Tk, Canvas, PhotoImage, filedialog, StringVar, Entry, Button, OptionMenu
from PIL import Image, ImageTk, ImageDraw, ImageFont

class PhotoStickerMaker:
    def __init__(self):
        self.root = Tk()
        self.root.title("Photo Sticker Maker")
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.pack()
        self.photo = None
        self.selected_shape = StringVar(self.root)
        self.text_input = Entry(self.root)
        self.text_input.pack()
        self.shape_dropdown = OptionMenu(self.root, self.selected_shape, "Circle", "Square", "Star")
        self.shape_dropdown.pack()
        self.create_buttons()
        self.root.mainloop()

    def create_buttons(self):
        Button(self.root, text="Import Photo", command=self.import_photo).pack()
        Button(self.root, text="Save Sticker", command=self.save_sticker).pack()
        Button(self.root, text="Crop Photo", command=lambda: self.crop_photo(50, 50, 200, 200)).pack()
        Button(self.root, text="Add Text", command=self.add_text).pack()
        Button(self.root, text="Resize Photo", command=lambda: self.resize_photo(400, 300)).pack()
        Button(self.root, text="Apply Effect", command=lambda: self.apply_effect("BLUR")).pack()

    def import_photo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.photo = Image.open(file_path)
            self.display_photo()

    def display_photo(self):
        if self.photo:
            self.tk_image = ImageTk.PhotoImage(self.photo)
            self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def select_shape(self, shape):
        self.selected_shape.set(shape)

    def set_size(self, width, height):
        if self.photo:
            self.photo = self.photo.resize((width, height))

    def add_text(self):
        if self.photo:
            draw = ImageDraw.Draw(self.photo)
            font = ImageFont.load_default()
            text = self.text_input.get()
            draw.text((10, 10), text, fill="black", font=font)
            self.display_photo()

    def add_decorative_element(self, element):
        pass  # Placeholder for additional decorative elements

    def crop_photo(self, x, y, width, height):
        if self.photo:
            self.photo = self.photo.crop((x, y, x + width, y + height))
            self.display_photo()

    def resize_photo(self, width, height):
        if self.photo:
            self.set_size(width, height)

    def apply_effect(self, effect):
        if self.photo:
            if effect == "BLUR":
                from PIL import ImageFilter
                self.photo = self.photo.filter(ImageFilter.BLUR)
            self.display_photo()

    def save_sticker(self, file_name="sticker.png"):
        if self.photo:
            save_path = os.path.join("stickers", file_name)
            self.photo.save(save_path, "PNG")

if __name__ == "__main__":
    if not os.path.exists("stickers"):
        os.makedirs("stickers")
    app = PhotoStickerMaker()