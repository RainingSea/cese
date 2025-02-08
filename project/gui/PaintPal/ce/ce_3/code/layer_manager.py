from layer import Layer

class LayerManager:
    def __init__(self):
        self.layers = []

    def create_layer(self, name: str) -> Layer:
        new_layer = Layer(name)
        self.layers.append(new_layer)
        return new_layer

    def delete_layer(self, layer: Layer) -> None:
        self.layers.remove(layer)

    def get_layers(self) -> list:
        return self.layers