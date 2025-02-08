import tkinter as tk
from tkinter import filedialog
from photo_editor import PhotoEditor

class Main:
    def __init__(self):
        self.photo_editor = PhotoEditor()
        self.root = tk.Tk()
        self.root.title("Sticker Maker")
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text='Import Photo', command=self.import_photo).pack()
        tk.Button(self.root, text='Choose Shape', command=self.choose_shape).pack()
        tk.Button(self.root, text='Set Size', command=self.set_size).pack()
        tk.Button(self.root, text='Add Text', command=self.add_text).pack()
        tk.Button(self.root, text='Add Decorative Elements', command=self.add_decorative_element).pack()
        tk.Button(self.root, text='Crop', command=self.crop_image).pack()
        tk.Button(self.root, text='Resize', command=self.resize_image).pack()
        tk.Button(self.root, text='Apply Effects', command=self.apply_effect).pack()
        tk.Button(self.root, text='Save as PNG', command=self.save_as_png).pack()

    def import_photo(self):
        file_path = filedialog.askopenfilename()
        self.photo_editor.import_photo(file_path)

    def choose_shape(self):
        # Placeholder for shape selection logic
        self.photo_editor.choose_shape("circle")

    def set_size(self):
        # Placeholder for size input logic
        self.photo_editor.set_size(200, 200)

    def add_text(self):
        # Placeholder for text input logic
        self.photo_editor.add_text("Sample Text", "Arial", "black")

    def add_decorative_element(self):
        # Placeholder for adding decorative elements
        pass

    def crop_image(self):
        # Placeholder for crop input logic
        self.photo_editor.crop_image(0, 0, 100, 100)

    def resize_image(self):
        # Placeholder for resize input logic
        self.photo_editor.resize_image(150, 150)

    def apply_effect(self):
        # Placeholder for effect selection logic
        self.photo_editor.apply_effect("grayscale")

    def save_as_png(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".png")
        self.photo_editor.save_as_png(file_name)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()