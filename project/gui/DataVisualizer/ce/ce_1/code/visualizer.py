import matplotlib.pyplot as plt

class Visualizer:
    def plot_bar_chart(self, data: list, options: dict):
        labels = data[0]
        values = list(map(float, data[1]))
        plt.bar(labels, values, color=options.get('color', 'blue'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.title(options.get('title', 'Bar Chart'))
        plt.show()

    def plot_line_graph(self, data: list, options: dict):
        labels = data[0]
        values = list(map(float, data[1]))
        plt.plot(labels, values, color=options.get('color', 'blue'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.title(options.get('title', 'Line Graph'))
        plt.show()

    def plot_scatter_plot(self, data: list, options: dict):
        x_values = list(map(float, data[0]))
        y_values = list(map(float, data[1]))
        plt.scatter(x_values, y_values, color=options.get('color', 'blue'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.title(options.get('title', 'Scatter Plot'))
        plt.show()

    def plot_pie_chart(self, data: list, options: dict):
        labels = data[0]
        sizes = list(map(float, data[1]))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(options.get('title', 'Pie Chart'))
        plt.show()