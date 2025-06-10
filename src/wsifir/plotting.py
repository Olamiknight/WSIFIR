from matplotlib import pyplot as plt
import numpy as np


def plot_grouped_bar_chart(df1, df2, title):
    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Set the bar width
    bar_width = 0.35

    # Set the x locations for the bars
    x = np.arange(len(df1))

    # Create the bars for df1
    plt.bar(
        x,
        df1["Mean"],
        yerr=df1["Standard Deviation"],
        width=bar_width,
        label="Initial",
    )

    # Create the bars for df2
    plt.bar(
        x + bar_width,
        df2["Mean"],
        yerr=df2["Standard Deviation"],
        width=bar_width,
        label="Registered",
    )

    # Add labels and title
    plt.xlabel("Metrics")
    plt.ylabel("Values")
    plt.title(title)
    plt.xticks(x + bar_width / 2, df1.index)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
