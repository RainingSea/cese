import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self):
        self.data = {}

    def import_data(self, file_path: str) -> None:
        self.data = pd.read_csv(file_path)

    def create_bar_chart(self) -> None:
        self.data.plot(kind='bar')
        plt.show()

    def create_line_graph(self) -> None:
        self.data.plot(kind='line')
        plt.show()

    def create_scatter_plot(self) -> None:
        plt.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1])
        plt.show()

    def create_pie_chart(self) -> None:
        self.data.plot(kind='pie', y=self.data.columns[0])
        plt.show()

    def customize_appearance(self, colors: list, labels: list) -> None:
        plt.gca().set_facecolor(colors[0])
        plt.xticks(ticks=range(len(labels)), labels=labels)

    def export_visualization(self, file_name: str) -> None:
        plt.savefig(file_name)