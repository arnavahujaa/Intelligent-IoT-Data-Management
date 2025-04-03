from bokeh.plotting import output_notebook, figure, show
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import MediumContrast3
from bokeh.transform import factor_cmap

output_notebook()

def grouped_bar_chart(df, category_col, value_cols):
    """
    Create a grouped bar chart using Bokeh.

    Parameters:
    df (pd.DataFrame): DataFrame containing categorical and numerical data.
    category_col (str): Column representing categories (e.g., time, labels).
    value_cols (list): List of numerical columns to group in bars.
    """
    categories = df[category_col].astype(str).tolist()
    values = {col: df[col].tolist() for col in value_cols}
    
    x = [(category, col) for category in categories for col in value_cols]
    counts = sum(zip(*[values[col] for col in value_cols]), ())  # Flatten list of tuples
    
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    
    p = figure(x_range=FactorRange(*x), height=350, title=f"Grouped Bar Chart: {category_col}",
               toolbar_location=None, tools="", output_backend="svg")
    
    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
           fill_color=factor_cmap('x', palette=MediumContrast3, factors=value_cols, start=1, end=2))
    
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    
    show(p, notebook_handle=True)  # This ensures the plot appears in the notebook

