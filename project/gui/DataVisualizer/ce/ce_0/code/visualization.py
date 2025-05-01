import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        self.data = []

    def create_bar_chart(self):
        if not self.data:
            return
        labels = [row[0] for row in self.data[1:]]
        values = [float(row[1]) for row in self.data[1:]]
        plt.bar(labels, values)
        plt.title("Bar Chart")
        plt.xlabel("Labels")
        plt.ylabel("Values")
        plt.show()

    def create_line_graph(self):
        if not self.data:
            return
        labels = [row[0] for row in self.data[1:]]
        values = [float(row[1]) for row in self.data[1:]]
        plt.plot(labels, values)
        plt.title("Line Graph")
        plt.xlabel("Labels")
        plt.ylabel("Values")
        plt.show()

    def create_scatter_plot(self):
        if not self.data:
            return
        labels = [row[0] for row in self.data[1:]]
        values = [float(row[1]) for row in self.data[1:]]
        plt.scatter(labels, values)
        plt.title("Scatter Plot")
        plt.xlabel("Labels")
        plt.ylabel("Values")
        plt.show()

    def create_pie_chart(self):
        if not self.data:
            return
        labels = [row[0] for row in self.data[1:]]
        values = [float(row[1]) for row in self.data[1:]]
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Pie Chart")
        plt.show()

    def customize_appearance(self, options: dict) -> None:
        # Placeholder for customization logic
        pass

    def export_image(self, file_path: str) -> None:
        plt.savefig(file_path)