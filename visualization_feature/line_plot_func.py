import matplotlib.pyplot as plt
import pandas as pd
import math

def line_plot(df, streams=None, start_time=None, end_time=None, normalise=False):
    """
    Create visualisations for data streams with automatic subfigure arrangement.
    
    Parameters:
    df (pd.DataFrame): DataFrame where columns represent data streams.
    streams (list): List of column names to plot. If None, plot all.
    start_time (str): Start time for filtering (if applicable, format: 'YYYY-MM-DD HH:MM:SS').
    end_time (str): End time for filtering (if applicable, format: 'YYYY-MM-DD HH:MM:SS').
    normalise (bool): If True, normalise all selected streams to [0,1] scale.
    """
    if streams is None:
        streams = df.columns.tolist()  # Select all columns if no specific streams are provided
    else:
        df = df[streams]  # Filter DataFrame to only selected streams
    
    if start_time and end_time:
        df = df.loc[start_time:end_time]  # Filter data based on the time window
    
    if normalise:
        df = (df - df.min()) / (df.max() - df.min())  # Normalize data to [0,1] scale
    
    num_streams = len(streams)
    rows = math.ceil(num_streams / 2)  # Define number of rows (2 subplots per row if possible)
    cols = min(2, num_streams)  # Define number of columns
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows), squeeze=False)
    axes = axes.flatten()  # Flatten axes for easy iteration
    
    for i, col in enumerate(streams):
        axes[i].plot(df.index, df[col], label=col)
        axes[i].set_title(f"Stream: {col}")
        axes[i].set_xlabel("Time")
        axes[i].set_ylabel("Value")
        for tick in axes[i].get_xticklabels():
            tick.set_rotation(45)  # Fix rotation issue
        axes[i].legend()
        axes[i].grid()
    
    plt.tight_layout()
    plt.show()