import tkinter as tk
from tkinter import filedialog, messagebox
from image_processor import ImageProcessor
import datetime
import os

class ImageEnhancer:
    def __init__(self, master):
        self.master = master
        self.image_processor = ImageProcessor()
        self.current_image_path = None

        self.create_widgets()

    def create_widgets(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Import Image", command=self.import_image)
        self.file_menu.add_command(label="Save Image", command=self.save_image)

        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack()

        self.brightness_slider = tk.Scale(self.master, from_=0, to=2, resolution=0.1, label="Brightness", orient=tk.HORIZONTAL, command=self.adjust_brightness)
        self.brightness_slider.pack()

        self.contrast_slider = tk.Scale(self.master, from_=0, to=2, resolution=0.1, label="Contrast", orient=tk.HORIZONTAL, command=self.adjust_contrast)
        self.contrast_slider.pack()

        self.saturation_slider = tk.Scale(self.master, from_=0, to=2, resolution=0.1, label="Saturation", orient=tk.HORIZONTAL, command=self.adjust_saturation)
        self.saturation_slider.pack()

    def import_image(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image_path = file_path
            self.image_processor.load_image(file_path)
            self.display_image()

    def display_image(self) -> None:
        if self.image_processor.image is not None:
            self.tk_image = ImageTk.PhotoImage(self.image_processor.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def adjust_brightness(self, value: float) -> None:
        self.image_processor.adjust_brightness(float(value))
        self.display_image()

    def adjust_contrast(self, value: float) -> None:
        self.image_processor.adjust_contrast(float(value))
        self.display_image()

    def adjust_saturation(self, value: float) -> None:
        self.image_processor.adjust_saturation(float(value))
        self.display_image()

    def save_image(self) -> None:
        if self.current_image_path:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.basename(self.current_image_path)
            new_file_name = f"{os.path.splitext(base_name)[0]}_{timestamp}.png"
            save_path = os.path.join(os.path.dirname(self.current_image_path), new_file_name)
            self.image_processor.save(save_path)
            messagebox.showinfo("Image Saved", f"Image saved as {new_file_name}")

def main():
    root = tk.Tk()
    app = ImageEnhancer(root)
    root.mainloop()

if __name__ == "__main__":
    main()