import tkinter as tk
from layer import Layer

class LayerManager(tk.Frame):
    def __init__(self, master, canvas):
        super().__init__(master)
        self.layers = []
        self.canvas = canvas
        self.create_widgets()

    def create_widgets(self):
        self.create_layer_button = tk.Button(self, text="Create Layer", command=self.create_layer)
        self.create_layer_button.pack()

        self.layer_listbox = tk.Listbox(self)
        self.layer_listbox.pack(fill=tk.BOTH, expand=True)

    def create_layer(self, name: str = "Layer"):
        new_layer = Layer(name)
        self.layers.append(new_layer)
        self.layer_listbox.insert(tk.END, name)
        self.canvas.add_layer(new_layer)

    def delete_layer(self, index: int):
        if 0 <= index < len(self.layers):
            del self.layers[index]
            self.layer_listbox.delete(index)

    def toggle_visibility(self, index: int):
        if 0 <= index < len(self.layers):
            self.layers[index].toggle_visibility()

    def reorder_layers(self, old_index: int, new_index: int):
        if 0 <= old_index < len(self.layers) and 0 <= new_index < len(self.layers):
            self.layers.insert(new_index, self.layers.pop(old_index))
            self.update_layer_listbox()

    def update_layer_listbox(self):
        self.layer_listbox.delete(0, tk.END)
        for layer in self.layers:
            self.layer_listbox.insert(tk.END, layer.name)