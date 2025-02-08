import tkinter as tk
from tkinter import filedialog, messagebox
from image_editor import ImageEditor

class Main:
    def __init__(self):
        self.editor = ImageEditor()
        self.window = tk.Tk()
        self.window.title("Image Editor")
        self.create_menu()
        self.create_canvas()
        self.window.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_image)
        file_menu.add_command(label="Save", command=self.save_image)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Adjust Brightness", command=self.adjust_brightness)
        edit_menu.add_command(label="Adjust Contrast", command=self.adjust_contrast)
        edit_menu.add_command(label="Adjust Saturation", command=self.adjust_saturation)
        edit_menu.add_command(label="Apply Filter", command=self.apply_filter)
        edit_menu.add_command(label="Crop", command=self.crop_image)
        edit_menu.add_command(label="Resize", command=self.resize_image)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.editor.load_image(file_path)
            self.display_image()

    def display_image(self):
        if self.editor.image:
            self.tk_image = self.editor.image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.editor.save_image(file_path)

    def adjust_brightness(self):
        value = self.get_float_input("Adjust Brightness", "Enter brightness value (0.0 - 2.0):")
        if value is not None:
            self.editor.adjust_brightness(value)
            self.display_image()

    def adjust_contrast(self):
        value = self.get_float_input("Adjust Contrast", "Enter contrast value (0.0 - 2.0):")
        if value is not None:
            self.editor.adjust_contrast(value)
            self.display_image()

    def adjust_saturation(self):
        value = self.get_float_input("Adjust Saturation", "Enter saturation value (0.0 - 2.0):")
        if value is not None:
            self.editor.adjust_saturation(value)
            self.display_image()

    def apply_filter(self):
        filter_type = self.get_string_input("Apply Filter", "Enter filter type (BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EMBOSS):")
        if filter_type:
            self.editor.apply_filter(filter_type)
            self.display_image()

    def crop_image(self):
        left = self.get_int_input("Crop Image", "Enter left coordinate:")
        upper = self.get_int_input("Crop Image", "Enter upper coordinate:")
        right = self.get_int_input("Crop Image", "Enter right coordinate:")
        lower = self.get_int_input("Crop Image", "Enter lower coordinate:")
        if left is not None and upper is not None and right is not None and lower is not None:
            self.editor.crop_image(left, upper, right, lower)
            self.display_image()

    def resize_image(self):
        width = self.get_int_input("Resize Image", "Enter new width:")
        height = self.get_int_input("Resize Image", "Enter new height:")
        if width is not None and height is not None:
            self.editor.resize_image(width, height)
            self.display_image()

    def get_float_input(self, title, prompt):
        return self.get_input(title, prompt, float)

    def get_int_input(self, title, prompt):
        return self.get_input(title, prompt, int)

    def get_string_input(self, title, prompt):
        return self.get_input(title, prompt, str)

    def get_input(self, title, prompt, input_type):
        input_value = simpledialog.askstring(title, prompt)
        if input_value is not None:
            try:
                return input_type(input_value)
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter a valid value.")
        return None

if __name__ == "__main__":
    Main()