import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, dataset_path: str = None):
        self.dataset_path = dataset_path
        self.visualization_type = None
        self.data = None

    def import_data(self, file_path: str) -> None:
        """Imports data from a CSV file."""
        self.data = pd.read_csv(file_path)
        self.dataset_path = file_path

    def create_visualization(self) -> None:
        """Creates a visualization based on the selected type."""
        if self.visualization_type == 'bar':
            self._create_bar_chart()
        elif self.visualization_type == 'line':
            self._create_line_graph()
        elif self.visualization_type == 'scatter':
            self._create_scatter_plot()
        elif self.visualization_type == 'pie':
            self._create_pie_chart()

    def customize_visualization(self, options: dict) -> None:
        """Customizes the visualization with provided options."""
        # Customization logic can be added here based on options
        pass

    def export_visualization(self, file_name: str) -> None:
        """Exports the current visualization to a PNG file."""
        plt.savefig(file_name)

    def _create_bar_chart(self) -> None:
        """Creates a bar chart from the data."""
        self.data.plot(kind='bar')
        plt.title('Bar Chart')
        plt.show()

    def _create_line_graph(self) -> None:
        """Creates a line graph from the data."""
        self.data.plot(kind='line')
        plt.title('Line Graph')
        plt.show()

    def _create_scatter_plot(self) -> None:
        """Creates a scatter plot from the data."""
        plt.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1])
        plt.title('Scatter Plot')
        plt.xlabel(self.data.columns[0])
        plt.ylabel(self.data.columns[1])
        plt.show()

    def _create_pie_chart(self) -> None:
        """Creates a pie chart from the data."""
        self.data.plot(kind='pie', y=self.data.columns[0], autopct='%1.1f%%')
        plt.title('Pie Chart')
        plt.show()