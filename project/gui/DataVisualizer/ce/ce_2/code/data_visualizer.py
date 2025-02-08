import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self):
        self.data_file = ""
        self.visualization_type = ""

    def import_data(self, file_path: str) -> dict:
        self.data_file = file_path
        data = pd.read_csv(file_path)
        return data.to_dict()

    def create_visualization(self):
        data = pd.read_csv(self.data_file)
        if self.visualization_type == "bar":
            data.plot(kind='bar')
        elif self.visualization_type == "line":
            data.plot(kind='line')
        elif self.visualization_type == "scatter":
            data.plot(kind='scatter', x=data.columns[0], y=data.columns[1])
        plt.show()

    def customize_visualization(self, options: dict):
        plt.title(options.get('title', 'Visualization'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        if 'color' in options:
            plt.gca().set_color_cycle(options['color'])

    def export_visualization(self, output_path: str):
        plt.savefig(output_path)