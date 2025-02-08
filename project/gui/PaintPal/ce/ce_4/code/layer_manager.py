from layer import Layer

class LayerManager:
    def __init__(self):
        self.layers = []

    def create_layer(self) -> Layer:
        new_layer = Layer(image=Image.new('RGBA', (800, 600), (255, 255, 255, 0)))
        self.layers.append(new_layer)
        return new_layer

    def delete_layer(self, layer: Layer):
        self.layers.remove(layer)

    def manipulate_layer(self, layer: Layer, action: str):
        # Logic for manipulating layers based on the action
        pass