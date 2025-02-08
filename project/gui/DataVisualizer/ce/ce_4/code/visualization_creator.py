import matplotlib.pyplot as plt

class VisualizationCreator:
    def create_bar_chart(self, data: dict, options: dict) -> None:
        """Creates a bar chart from the provided data and customization options."""
        plt.bar(data['labels'], data['values'], color=options.get('color', 'blue'))
        plt.title(options.get('title', 'Bar Chart'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.show()

    def create_line_graph(self, data: dict, options: dict) -> None:
        """Creates a line graph from the provided data and customization options."""
        plt.plot(data['labels'], data['values'], color=options.get('color', 'blue'))
        plt.title(options.get('title', 'Line Graph'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.show()

    def create_scatter_plot(self, data: dict, options: dict) -> None:
        """Creates a scatter plot from the provided data and customization options."""
        plt.scatter(data['x_values'], data['y_values'], color=options.get('color', 'blue'))
        plt.title(options.get('title', 'Scatter Plot'))
        plt.xlabel(options.get('xlabel', 'X-axis'))
        plt.ylabel(options.get('ylabel', 'Y-axis'))
        plt.show()

    def create_pie_chart(self, data: dict, options: dict) -> None:
        """Creates a pie chart from the provided data and customization options."""
        plt.pie(data['values'], labels=data['labels'], colors=options.get('colors', None), autopct='%1.1f%%')
        plt.title(options.get('title', 'Pie Chart'))
        plt.show()