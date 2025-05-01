import tkinter as tk
from tkinter import filedialog, messagebox
import json
from image_processor import ImageProcessor

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.image_processor = ImageProcessor()
        
        self.create_menu()
        self.create_widgets()
        self.load_settings()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import Image", command=self.import_image)
        file_menu.add_command(label="Save Image", command=self.save_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.brightness_slider = tk.Scale(self.root, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL, command=self.adjust_brightness)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.root, from_=-100, to=100, label="Contrast", orient=tk.HORIZONTAL, command=self.adjust_contrast)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.root, from_=-100, to=100, label="Saturation", orient=tk.HORIZONTAL, command=self.adjust_saturation)
        self.saturation_slider.pack()

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.image_processor.image:
            self.canvas.delete("all")
            self.tk_image = self.image_processor.image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def adjust_brightness(self, value):
        self.image_processor.adjust_brightness(int(value))
        self.display_image()

    def adjust_contrast(self, value):
        self.image_processor.adjust_contrast(int(value))
        self.display_image()

    def adjust_saturation(self, value):
        self.image_processor.adjust_saturation(int(value))
        self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.image_processor.save_image(file_path)

    def load_settings(self):
        try:
            with open("settings.json", "r") as settings_file:
                settings = json.load(settings_file)
                last_image_path = settings.get("last_image_path")
                if last_image_path:
                    self.image_processor.load_image(last_image_path)
                    self.display_image()
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def on_closing(self):
        settings = {"last_image_path": self.image_processor.image_path}
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = Main(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()