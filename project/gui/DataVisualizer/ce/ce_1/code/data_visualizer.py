from data_loader import DataLoader
from visualizer import Visualizer

class DataVisualizer:
    def __init__(self):
        self.data_loader = DataLoader()
        self.visualizer = Visualizer()

    def import_data(self, file_path: str):
        return self.data_loader.load_data(file_path)

    def create_visualization(self, visualization_type: str, data: list, options: dict):
        if visualization_type == 'bar':
            self.visualizer.plot_bar_chart(data, options)
        elif visualization_type == 'line':
            self.visualizer.plot_line_graph(data, options)
        elif visualization_type == 'scatter':
            self.visualizer.plot_scatter_plot(data, options)
        elif visualization_type == 'pie':
            self.visualizer.plot_pie_chart(data, options)

    def customize_visualization(self, options: dict):
        # Customization logic can be added here
        pass

    def export_visualization(self, file_path: str):
        # Export logic can be added here
        pass