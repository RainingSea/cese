import matplotlib.pyplot as plt

class Visualization:
    def draw_bar_chart(self, data):
        data.plot(kind='bar')
        plt.show()

    def draw_line_graph(self, data):
        data.plot(kind='line')
        plt.show()

    def draw_scatter_plot(self, data):
        data.plot(kind='scatter', x=data.columns[0], y=data.columns[1])
        plt.show()

    def draw_pie_chart(self, data):
        data.iloc[:, 0].value_counts().plot(kind='pie')
        plt.show()

    def export(self, file_path: str) -> None:
        plt.savefig(file_path)