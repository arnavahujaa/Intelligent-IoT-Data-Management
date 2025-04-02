import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def correlation_based(df, streams, start_date, end_date, threshold=None):
    """
    Analyze streams to detect outliers based on the correlation between the streams.

    Parameters:
    - df: DataFrame containing data with 'created_at' column already set as the index.
    - streams: List of column names (streams) to analyze (at least 3 streams).
    - start_date: Start time (str or datetime).
    - end_date: End time (str or datetime).
    - threshold: Threshold to determine an outlier. If not provided, the value (mean - std) of the average correlations is used.

    Returns:
    - A dictionary with keys as stream names and values as a dict containing average correlation (avg_corr)
      and flag 'is_outlier' (True/False).
    """

    # Check the number of streams
    if len(streams) < 3:
        raise ValueError("At least 3 streams are required to analyze outliers.")

    # Filter the data for the given time period
    df_period = df.loc[start_date:end_date, streams]

    # Calculate the correlation matrix between the streams
    corr_matrix = df_period.corr()

    # Compute the average correlation for each stream with the other streams
    avg_corr = {}
    for stream in streams:
        # Exclude self-correlation (always 1)
        other_corr = corr_matrix.loc[stream, streams].drop(stream)
        avg_corr[stream] = other_corr.mean()

    avg_corr_series = pd.Series(avg_corr)

    # If no threshold is provided, use mean - std of the average correlations
    if threshold is None:
        threshold = avg_corr_series.mean() - avg_corr_series.std()

    # Identify streams with average correlation lower than the threshold (suspected anomaly)
    outlier_streams = avg_corr_series[avg_corr_series < threshold]

    # Print the analysis results
    print("Average correlation of each stream:")
    print(avg_corr_series)
    print("\nOutlier threshold:", threshold)
    print("\nSuspected outlier streams:")
    print(outlier_streams)

    # Return the results as a dictionary
    results = {stream: {"avg_corr": avg_corr_series[stream], "is_outlier": avg_corr_series[stream] < threshold}
               for stream in streams}
    return results


def volatility_based(df, streams, start_date, end_date, threshold=None):
    """
    Detect outliers based on the volatility (standard deviation) of each stream.

    The volatility of each stream is calculated over the specified period.
    We use the negative of the standard deviation as the metric (since higher volatility results in a lower negative value).
    If this metric is lower than the threshold (computed as mean - std of the metric), the stream is flagged as an outlier.

    Note: The computed metric is stored in the key 'avg_corr' to maintain a consistent output format.

    Parameters:
    - df: DataFrame containing data with 'created_at' as index.
    - streams: List of column names (streams) to analyze (at least 3 streams).
    - start_date: Start time (str or datetime).
    - end_date: End time (str or datetime).
    - threshold: Threshold to determine an outlier. If not provided, the value (mean - std) of the metric is used.

    Returns:
    - A dictionary with keys as stream names and values as a dict containing:
      - avg_corr: The negative standard deviation of the stream.
      - is_outlier: True if the stream is detected as an outlier.
    """

    if len(streams) < 3:
        raise ValueError("At least 3 streams are required for analysis.")

    # Filter data for the specified time period and streams
    df_period = df.loc[start_date:end_date, streams]

    # Calculate the standard deviation (volatility) for each stream
    volatility = df_period.std()
    # Invert the standard deviation to follow the same criteria: lower value indicates anomaly
    volatility_metric = -volatility

    # If threshold not provided, calculate it as (mean - std) of the volatility metric
    if threshold is None:
        threshold = volatility_metric.mean() - volatility_metric.std()

    print("Volatility (std) of each stream (inverted):")
    print(volatility_metric)
    print("\nOutlier threshold:", threshold)
    print("\nSuspected outlier streams (abnormal volatility):")
    print(volatility_metric[volatility_metric < threshold])

    results = {stream: {"avg_corr": volatility_metric[stream],
                        "is_outlier": volatility_metric[stream] < threshold}
               for stream in streams}
    return results


def mean_based(df, streams, start_date, end_date, threshold=None):
    """
    Detect outliers based on the mean value of each stream.

    Each stream is evaluated by its average value over the specified time period.
    If the average value of a stream is lower than the threshold (computed as mean - std of the average values),
    the stream is flagged as an outlier.

    Note: For consistency, the computed average is stored in the key 'avg_corr'.

    Parameters:
    - df: DataFrame containing data with 'created_at' as index.
    - streams: List of column names (streams) to analyze (at least 3 streams).
    - start_date: Start time (str or datetime).
    - end_date: End time (str or datetime).
    - threshold: Threshold to determine an outlier. If not provided, the value (mean - std) of the average values is used.

    Returns:
    - A dictionary with keys as stream names and values as a dict containing:
      - avg_corr: The average value of the stream.
      - is_outlier: True if the stream is detected as an outlier.
    """

    if len(streams) < 3:
        raise ValueError("At least 3 streams are required for analysis.")

    # Filter data for the specified time period and streams
    df_period = df.loc[start_date:end_date, streams]

    # Calculate the mean value for each stream
    avg_values = df_period.mean()

    # If threshold not provided, calculate it as (mean - std) of the average values
    if threshold is None:
        threshold = avg_values.mean() - avg_values.std()

    print("Mean value of each stream:")
    print(avg_values)
    print("\nOutlier threshold:", threshold)
    print("\nSuspected outlier streams (low mean):")
    print(avg_values[avg_values < threshold])

    results = {stream: {"avg_corr": avg_values[stream],
                        "is_outlier": avg_values[stream] < threshold}
               for stream in streams}
    return results
