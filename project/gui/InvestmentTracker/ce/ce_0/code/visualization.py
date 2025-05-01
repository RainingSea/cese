import matplotlib.pyplot as plt

def plot_investment_performance(investments, canvas):
    names = [investment.name for investment in investments]
    amounts = [investment.amount for investment in investments]

    plt.figure(figsize=(5, 3))
    plt.bar(names, amounts)
    plt.title("Investment Performance")
    plt.xlabel("Investments")
    plt.ylabel("Amount")

    plt.savefig('temp_plot.png')
    plt.close()

    # Load the plot into the tkinter canvas
    canvas.create_image(0, 0, anchor='nw', image=tk.PhotoImage(file='temp_plot.png'))