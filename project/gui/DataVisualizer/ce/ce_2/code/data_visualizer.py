import pandas as pd
import matplotlib.pyplot as plt
from data_frame import DataFrame

class DataVisualizer:
    def __init__(self):
        self.data = DataFrame()

    def import_data(self, file_path: str) -> None:
        self.data.load_data(file_path)

    def create_visualization(self, type: str) -> None:
        data = self.data.get_data()
        if type == "Bar Chart":
            plt.bar(range(len(data)), data)
        elif type == "Line Graph":
            plt.plot(data)
        elif type == "Scatter Plot":
            plt.scatter(range(len(data)), data)
        elif type == "Pie Chart":
            plt.pie(data)
        plt.show()

    def customize_visualization(self, colors: list, labels: list, title: str) -> None:
        plt.title(title)
        plt.xticks(range(len(labels)), labels)
        plt.gca().set_facecolor(colors[0])  # Example of customizing color

    def export_visualization(self, file_path: str) -> None:
        plt.savefig(file_path)

    def visualize(self, type: str) -> None:
        self.create_visualization(type)