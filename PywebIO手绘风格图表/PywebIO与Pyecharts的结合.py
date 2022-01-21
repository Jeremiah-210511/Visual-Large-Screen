import pyecharts.options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from cutecharts.faker import Faker
from pyecharts.charts import Grid

from pywebio import start_server
from pywebio.output import put_html


def bar_plots():
    bar = (
        Bar()
            .add_xaxis(Faker.choose())
            .add_yaxis("商家A", Faker.values())
            .add_yaxis("商家B", Faker.values())
            .set_global_opts(title_opts=opts.TitleOpts(title="Grid-Bar"))
    )
    return bar

def line_plots():
    line = (
        Line()
            .add_xaxis(Faker.choose())
            .add_yaxis("商家A", Faker.values())
            .add_yaxis("商家B", Faker.values())
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Grid-Line", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="48%"),
        )
    )
    return line

def main():
    c = (
        Grid()
            .add(bar_plots(), grid_opts=opts.GridOpts(pos_bottom="60%"))
            .add(line_plots(), grid_opts=opts.GridOpts(pos_top="60%"))
    )
    c.width = "100%"
    put_html(c.render_notebook())

if __name__ == '__main__':
    start_server(main, debug=True, port=8080)