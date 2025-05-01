import pandas as pd
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self):
        self.data = pd.DataFrame()

    def set_data(self, data: pd.DataFrame) -> None:
        self.data = data

    def create_bar_chart(self) -> None:
        if not self.data.empty:
            self.data.plot(kind='bar')
            plt.title("Bar Chart")
            plt.show()
        else:
            print("No data available for visualization.")

    def create_line_graph(self) -> None:
        if not self.data.empty:
            self.data.plot(kind='line')
            plt.title("Line Graph")
            plt.show()
        else:
            print("No data available for visualization.")

    def create_scatter_plot(self) -> None:
        if not self.data.empty:
            plt.scatter(self.data.iloc[:, 0], self.data.iloc[:, 1])
            plt.title("Scatter Plot")
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.grid(True)  # Enable grid lines
            plt.show()
        else:
            print("No data available for visualization.")

    def create_pie_chart(self) -> None:
        if not self.data.empty:
            self.data.iloc[:, 0].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
            plt.title("Pie Chart")
            plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular
            plt.show()
        else:
            print("No data available for visualization.")

    def customize_visualization(self, title: str, labels: list, colors: list) -> None:
        plt.title(title)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.gca().set_facecolor(colors[0])

    def export_visualization(self, file_name: str) -> None:
        plt.savefig(file_name)