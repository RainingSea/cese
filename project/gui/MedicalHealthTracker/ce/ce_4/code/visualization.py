import matplotlib.pyplot as plt

def plot_data(dates: list, values: list, title: str, ylabel: str) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()