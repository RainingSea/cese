import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import ImageTk
from image_processor import ImageProcessor
from sticker_creator import StickerCreator
from user_preferences import UserPreferences

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Sticker Maker")
        self.image_processor = ImageProcessor()
        self.sticker_creator = StickerCreator()
        self.user_preferences = UserPreferences()
        
        self.create_widgets()
        self.load_user_preferences()

    def create_widgets(self):
        self.import_button = tk.Button(self.root, text="Import Photo", command=self.import_photo)
        self.import_button.pack()

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.shape_menu = tk.StringVar(self.root)
        self.shape_menu.set("Select Shape")
        self.shape_dropdown = tk.OptionMenu(self.root, self.shape_menu, "Circle", "Square", "Star", command=self.select_shape)
        self.shape_dropdown.pack()

        self.size_entry = tk.Entry(self.root)
        self.size_entry.pack()

        self.text_entry = tk.Entry(self.root)
        self.text_entry.pack()

        self.color_button = tk.Button(self.root, text="Choose Text Color", command=self.choose_color)
        self.color_button.pack()

        self.preview_button = tk.Button(self.root, text="Preview", command=self.preview_sticker)
        self.preview_button.pack()

        self.save_button = tk.Button(self.root, text="Save Sticker", command=self.save_sticker)
        self.save_button.pack()

        self.crop_button = tk.Button(self.root, text="Crop Photo", command=self.crop_photo)
        self.crop_button.pack()

        self.resize_button = tk.Button(self.root, text="Resize Photo", command=self.resize_photo)
        self.resize_button.pack()

    def import_photo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.load_image(file_path)
            self.update_canvas()

    def update_canvas(self):
        if self.image_processor.image:
            self.canvas.delete("all")
            self.tk_image = ImageTk.PhotoImage(self.image_processor.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def select_shape(self, shape: str):
        self.sticker_creator.select_shape(shape)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.sticker_creator.add_text(self.text_entry.get(), color)

    def preview_sticker(self):
        sticker_image = self.sticker_creator.create_sticker(self.image_processor.image)
        sticker_image.show()

    def save_sticker(self):
        filename = f"stickers/sticker_{self.image_processor.get_timestamp()}.png"
        sticker_image = self.sticker_creator.create_sticker(self.image_processor.image)
        self.sticker_creator.save_sticker(sticker_image, filename)

    def crop_photo(self):
        dimensions = self.get_crop_dimensions()
        if dimensions:
            cropped_image = self.image_processor.crop(dimensions)
            if cropped_image:
                self.image_processor.image = cropped_image
                self.update_canvas()

    def resize_photo(self):
        dimensions = self.get_resize_dimensions()
        if dimensions:
            resized_image = self.image_processor.resize(dimensions)
            if resized_image:
                self.image_processor.image = resized_image
                self.update_canvas()

    def get_crop_dimensions(self):
        try:
            dimensions = self.size_entry.get().split(',')
            x1, y1 = map(int, dimensions[0].split('x'))
            x2, y2 = map(int, dimensions[1].split('x'))
            return (x1, y1, x2, y2)
        except Exception as e:
            messagebox.showerror("Error", "Invalid crop dimensions. Format: x1,y1,x2,y2")
            return None

    def get_resize_dimensions(self):
        try:
            dimensions = self.size_entry.get().split(',')
            width, height = map(int, dimensions)
            return (width, height)
        except Exception as e:
            messagebox.showerror("Error", "Invalid resize dimensions. Format: width,height")
            return None

    def load_user_preferences(self):
        preferences = self.user_preferences.load_preferences()
        if preferences:
            self.shape_menu.set(preferences.get('last_shape', 'Select Shape'))
            self.text_entry.insert(0, preferences.get('last_text', ''))
            self.size_entry.insert(0, preferences.get('last_size', '100,100'))

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()