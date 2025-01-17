from data_visualizer import DataVisualizer

def main() -> str:
    data_visualizer = DataVisualizer()
    # Example usage:
    data = data_visualizer.import_data('sample_data.csv')
    options = {'color': 'green', 'xlabel': 'Categories', 'ylabel': 'Values', 'title': 'Sample Bar Chart'}
    data_visualizer.create_visualization('bar', data, options)
    return "Visualization created."

if __name__ == "__main__":
    main()