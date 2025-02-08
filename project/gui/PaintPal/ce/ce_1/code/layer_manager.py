class Layer:
    def __init__(self, name: str):
        self.name = name
        self.visible = True

class LayerManager:
    def __init__(self):
        self.layers = []

    def add_layer(self) -> None:
        layer_name = f"Layer {len(self.layers) + 1}"
        self.layers.append(Layer(layer_name))

    def delete_layer(self, index: int) -> None:
        if 0 <= index < len(self.layers):
            del self.layers[index]

    def get_layers(self):
        return self.layers