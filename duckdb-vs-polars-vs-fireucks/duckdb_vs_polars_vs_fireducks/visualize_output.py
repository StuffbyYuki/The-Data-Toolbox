import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_output(data, file_type):
    sns.set_style(style=None)
    df = pl.DataFrame(
        data, schema=["time in seconds", "query type", "library"], orient="row"
    )
    plt.figure(figsize=(20, 8))
    ax = sns.barplot(
        df,
        x="query type",
        y="time in seconds",
        hue="library",
        errorbar=None,
        palette=["#FFF208", "#0A5301", "#075AFE"],
    )

    for container in ax.containers:
        ax.bar_label(container)

    ax.set(xlabel="", ylabel="Time in Seconds")
    plt.title(f"DuckDB vs Polars vs Fireducks - Speed Comparison ({file_type})")
    plt.savefig(f"output_{file_type}.png")
    plt.show()
