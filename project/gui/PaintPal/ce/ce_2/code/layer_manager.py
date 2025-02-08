import tkinter as tk
from layer import Layer

class LayerManager:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.layers = []
        self.layer_frame = tk.Frame(root)
        self.layer_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_layer_management()

    def create_layer_management(self):
        add_layer_button = tk.Button(self.layer_frame, text="Add Layer", command=self.add_layer)
        add_layer_button.pack(side=tk.TOP)

        delete_layer_button = tk.Button(self.layer_frame, text="Delete Layer", command=self.delete_layer)
        delete_layer_button.pack(side=tk.TOP)

    def add_layer(self, layer_id=None):
        new_layer = Layer(id=len(self.layers))
        self.layers.append(new_layer)

    def delete_layer(self, layer_id):
        if layer_id < len(self.layers):
            del self.layers[layer_id]