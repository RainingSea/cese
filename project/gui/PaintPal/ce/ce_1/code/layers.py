class Layer:
    def __init__(self, name="Layer"):
        self.name = name
        self.visible = True

class LayerManager:
    def __init__(self):
        self.layers = []

    def create_layer(self) -> Layer:
        new_layer = Layer()
        self.layers.append(new_layer)
        return new_layer

    def delete_layer(self, layer: Layer):
        if layer in self.layers:
            self.layers.remove(layer)

    def manipulate_layer(self, layer: Layer, action: str):
        # Logic to manipulate layer based on action
        pass