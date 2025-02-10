import matplotlib.pyplot as plt

class Trend:
    def plot_trends(self, results: list) -> None:
        dates = [result[0] for result in results]
        values = [result[1] for result in results]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, marker='o')
        plt.title('Medical Test Results Trend')
        plt.xlabel('Date')
        plt.ylabel('Result')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/trend.png')
        plt.close()