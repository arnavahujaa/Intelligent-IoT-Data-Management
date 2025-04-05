import matplotlib.pyplot as plt
import pandas as pd
import math

def boxplot(df, streams=None):
    """
    Create boxplots for selected data streams with automatic subfigure arrangement.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    streams (list): List of column names to plot. If None, plot all columns.
    """
    if streams is None:
        streams = df.columns.tolist()
    else:
        df = df[streams]
    
    num_streams = len(streams)
    rows = math.ceil(num_streams / 2)  # Define number of rows (2 subplots per row if possible)
    cols = min(2, num_streams)  # Define number of columns
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows), squeeze=False)
    axes = axes.flatten()  # Flatten axes for easy iteration
    
    for i, col in enumerate(streams):
        axes[i].boxplot(df[col].dropna(), vert=True)
        axes[i].set_title(f"Boxplot: {col}")
        axes[i].set_ylabel("Value")
        axes[i].grid()
    
    plt.tight_layout()
    plt.show()