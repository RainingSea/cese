from data_handler import DataHandler
from visualization_creator import VisualizationCreator

class DataVisualizer:
    def __init__(self):
        self.data_handler = DataHandler()
        self.visualization_creator = VisualizationCreator()

    def import_data(self, file_path: str) -> None:
        """Imports data from a CSV file."""
        self.data = self.data_handler.read_data(file_path)

    def create_visualization(self, visualization_type: str) -> None:
        """Creates a visualization based on the specified type."""
        if visualization_type == 'bar':
            self.visualization_creator.create_bar_chart(self.data, {})
        elif visualization_type == 'line':
            self.visualization_creator.create_line_graph(self.data, {})
        elif visualization_type == 'scatter':
            self.visualization_creator.create_scatter_plot(self.data, {})
        elif visualization_type == 'pie':
            self.visualization_creator.create_pie_chart(self.data, {})
        else:
            raise ValueError("Invalid visualization type")

    def customize_visualization(self, options: dict) -> None:
        """Customizes the visualization based on provided options."""
        self.options = options

    def export_visualization(self, file_name: str) -> None:
        """Exports the current visualization to a PNG file."""
        plt.savefig(file_name)