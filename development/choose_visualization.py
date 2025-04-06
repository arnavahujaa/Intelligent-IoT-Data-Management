import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualizations.grouped_bar_chart import grouped_bar_chart
from visualizations.line_plot import line_plot
from visualizations.box_plot import box_plot

def choose_visualization(df, streams=None, start_date=None, end_date=None, type='grouped_bar_chart'):
    if type == 'grouped_bar_chart':
        return grouped_bar_chart(df, streams, start_date, end_date)
    if type == 'line_plot':
        return line_plot(df, streams, start_date, end_date)
    if type == 'box_plot':
        return box_plot(df, streams)
    else:
        raise ValueError('Not a valid visualization type')