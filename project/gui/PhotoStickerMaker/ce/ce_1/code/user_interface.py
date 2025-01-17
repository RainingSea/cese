import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class UserInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Sticker Maker")
        self.canvas = tk.Canvas(master, width=500, height=500, bg='white')
        self.canvas.pack()
        self.image_on_canvas = None
        self.current_image = None

        self.setup_buttons()

    def setup_buttons(self):
        import_button = tk.Button(self.master, text="Import Image", command=self.import_image)
        import_button.pack(side=tk.LEFT)

        save_button = tk.Button(self.master, text="Save Sticker", command=self.save_sticker)
        save_button.pack(side=tk.LEFT)

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_image = Image.open(file_path)
            self.update_canvas(self.current_image)

    def save_sticker(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                       filetypes=[("PNG files", "*.png")])
            if file_path:
                self.current_image.save(file_path, "PNG")
                messagebox.showinfo("Success", "Sticker saved successfully!")

    def show_canvas(self):
        self.canvas.pack()

    def show_options(self):
        pass

    def update_canvas(self, image: Image):
        self.canvas.delete("all")
        self.image_on_canvas = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_on_canvas)