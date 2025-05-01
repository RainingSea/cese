import tkinter as tk

class LayerManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.layers = []
        self.create_widgets()

    def create_widgets(self):
        self.create_layer_button = tk.Button(self, text="Create Layer", command=self.create_layer)
        self.create_layer_button.pack()

        self.delete_layer_button = tk.Button(self, text="Delete Layer", command=lambda: self.delete_layer(0))
        self.delete_layer_button.pack()

    def create_layer(self):
        layer_id = len(self.layers) + 1
        self.layers.append(f"Layer {layer_id}")
        print(f"Created {self.layers[-1]}")

    def delete_layer(self, layer_id: int):
        if 0 <= layer_id < len(self.layers):
            print(f"Deleted {self.layers[layer_id]}")
            del self.layers[layer_id]