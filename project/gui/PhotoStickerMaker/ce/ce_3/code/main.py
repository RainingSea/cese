import json
from tkinter import Tk, Canvas, Button, filedialog, Frame, Text
from PIL import Image, ImageTk
from shapes import Shapes
from effects import Effects

class ImageProcessor:
    """Class to handle image processing tasks."""
    
    @staticmethod
    def crop_image(image: Image, crop_area: tuple) -> Image:
        """Crop the image to the specified area."""
        return image.crop(crop_area)

    @staticmethod
    def resize_image(image: Image, size: tuple) -> Image:
        """Resize the image to the specified size."""
        return image.resize(size)

    @staticmethod
    def apply_effect(image: Image, effect: str) -> Image:
        """Apply the specified effect to the image."""
        if effect == "blur":
            return Effects.apply_blur(image)
        elif effect == "sharpen":
            return Effects.apply_sharpen(image)
        return image

class StickerDesigner:
    """Class to design stickers."""
    
    def __init__(self):
        self.shapes = Shapes()
        self.text_elements = []

    def select_shape(self, shape: str):
        """Select a shape for the sticker."""
        if shape in self.shapes.shapes:
            return self.shapes.shapes[shape](size=(100, 100))  # Example size

    def set_size(self, size: tuple):
        """Set the size of the sticker."""
        self.size = size

    def add_text(self, text: str, font: str, color: str):
        """Add text to the sticker."""
        self.text_elements.append({"text": text, "font": font, "color": color})

    def add_decorative_element(self, element: str):
        """Add a decorative element to the sticker."""
        # Placeholder for decorative elements
        pass

    def generate_sticker(self) -> Image:
        """Generate the final sticker image."""
        # Placeholder for generating sticker image
        return Image.new('RGBA', (200, 200), (255, 255, 255, 0))

class Main:
    """Main class to initialize the application."""
    
    def __init__(self):
        self.root = Tk()
        self.image_processor = ImageProcessor()
        self.sticker_designer = StickerDesigner()
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main application widgets."""
        Button(self.root, text="Import Photo", command=self.import_photo).pack()
        Button(self.root, text="Save Sticker", command=self.save_sticker).pack()
        
    def import_photo(self):
        """Import a photo from the file system."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image = Image.open(file_path)
            self.display_image(self.current_image)

    def display_image(self, image: Image):
        """Display the image on the canvas."""
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def save_sticker(self):
        """Save the final sticker as a PNG file."""
        sticker = self.sticker_designer.generate_sticker()
        sticker.save("sticker.png", "PNG")
        
    def main(self):
        """Run the main application loop."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()