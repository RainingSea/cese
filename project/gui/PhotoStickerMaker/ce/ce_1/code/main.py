import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk

class Main:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Photo Sticker Maker")
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(side=tk.RIGHT)

        self.panel = tk.Frame(self.root)
        self.panel.pack(side=tk.LEFT)

        self.import_button = tk.Button(self.panel, text="Import Image", command=self.import_image)
        self.import_button.pack()

        self.shape_var = tk.StringVar(value="Circle")
        self.shape_menu = tk.OptionMenu(self.panel, self.shape_var, "Circle", "Square", "Star")
        self.shape_menu.pack()

        self.size_label = tk.Label(self.panel, text="Size:")
        self.size_label.pack()
        self.size_entry = tk.Entry(self.panel)
        self.size_entry.pack()

        self.text_label = tk.Label(self.panel, text="Text:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self.panel)
        self.text_entry.pack()

        self.font_label = tk.Label(self.panel, text="Font:")
        self.font_label.pack()
        self.font_entry = tk.Entry(self.panel)
        self.font_entry.pack()

        self.color_label = tk.Label(self.panel, text="Color:")
        self.color_label.pack()
        self.color_entry = tk.Entry(self.panel)
        self.color_entry.pack()

        self.add_text_button = tk.Button(self.panel, text="Add Text", command=self.add_text)
        self.add_text_button.pack()

        self.save_button = tk.Button(self.panel, text="Save Sticker", command=self.save_sticker)
        self.save_button.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename()
        self.image_processor.import_image(file_path)
        self.display_image()

    def display_image(self):
        img = Image.open(self.image_processor.image)
        img.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def add_text(self):
        content = self.text_entry.get()
        font_name = self.font_entry.get()
        color = self.color_entry.get()
        self.sticker_creator.add_text(content, font_name, color)

    def save_sticker(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        self.sticker_creator.save_sticker(file_name)

    def main(self):
        self.root.mainloop()

class ImageProcessor:
    def __init__(self):
        self.image = None

    def import_image(self, file_path: str) -> None:
        self.image = file_path

    def crop(self, x: int, y: int, width: int, height: int) -> None:
        img = Image.open(self.image)
        self.image = img.crop((x, y, x + width, y + height))

    def resize(self, width: int, height: int) -> None:
        img = Image.open(self.image)
        self.image = img.resize((width, height))

    def apply_effect(self, effect: str) -> None:
        img = Image.open(self.image)
        if effect == "grayscale":
            self.image = img.convert("L")
        # More effects can be added here

class StickerCreator:
    def __init__(self):
        self.shape = None
        self.size = None
        self.text = None

    def choose_shape(self, shape: str) -> None:
        self.shape = shape

    def set_size(self, width: int, height: int) -> None:
        self.size = (width, height)

    def add_text(self, content: str, font: str, color: str) -> None:
        self.text = (content, font, color)

    def add_decorative_element(self, element: str) -> None:
        # Implementation for adding decorative elements
        pass

    def save_sticker(self, file_name: str) -> None:
        # Implementation for saving the sticker as a PNG file
        # This would include drawing the shape, text, and any decorative elements
        pass

if __name__ == "__main__":
    app = Main()
    app.main()