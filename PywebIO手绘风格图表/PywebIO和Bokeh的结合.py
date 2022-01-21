from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.plotting import figure

from pywebio import start_server

def bar_plots():

    output_notebook(notebook_type='pywebio')
    fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    counts = [5, 3, 4, 2, 4, 6]

    p = figure(x_range=fruits, plot_height=350, title="Fruit Counts",
               toolbar_location=None, tools="")

    p.vbar(x=fruits, top=counts, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

if __name__ == "__main__":
    start_server(bar_plots, debug=True, port=8080)