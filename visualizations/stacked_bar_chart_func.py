import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import AutoDateLocator, DateFormatter

def plot_stacked_bar_chart(df, category_col, value_cols, title="Stacked Bar Chart"):
    """
    Create a stacked bar chart using Matplotlib with automatic date formatting.

    Parameters:
    df (pd.DataFrame): DataFrame containing categorical and numerical data.
    category_col (str): Column representing categories (x-axis).
    value_cols (list): List of numerical columns to stack.
    title (str): Title of the plot.
    """
    if category_col in df.index.names:
        df.reset_index(inplace=True)
    
    # Convert category column to datetime if not already
    df[category_col] = pd.to_datetime(df[category_col])

    # Set figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define x locations (timestamps)
    x = df[category_col]
    bottom = np.zeros(len(df))  # Start stacking from zero

    # Plot each value column as a stacked bar
    for col in value_cols:
        ax.bar(x, df[col], label=col, bottom=bottom)
        bottom += df[col]  # Update bottom for stacking

    # Automatically format x-axis for dates
    ax.xaxis.set_major_locator(AutoDateLocator())  # Auto-adjust tick positions
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  # Format date labels

    # Formatting
    ax.set_xlabel(category_col)
    ax.set_ylabel("Values")
    ax.set_title(title)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability

    # Show the plot
    plt.show()