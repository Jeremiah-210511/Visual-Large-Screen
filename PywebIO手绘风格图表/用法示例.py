from cutecharts.charts import Bar
from cutecharts.charts import Pie
from cutecharts.charts import Radar
from cutecharts.charts import Line
from cutecharts.charts import Scatter
from cutecharts.components import Page
from cutecharts.faker import Faker

from pywebio import start_server
from pywebio.output import put_html

def bar_base() -> Bar:
    chart = Bar("Bar-基本示例", width="100%")
    chart.set_options(labels=Faker.choose(), x_label="I'm xlabel", y_label="I'm ylabel")
    chart.add_series("series-A", Faker.values())
    return chart

def pie_base() -> Pie:
    chart = Pie("Pie-基本示例", width="100%")
    chart.set_options(labels=Faker.choose())
    chart.add_series(Faker.values())
    return chart

def radar_base() -> Radar:
    chart = Radar("Radar-基本示例", width="100%")
    chart.set_options(labels=Faker.choose())
    chart.add_series("series-A", Faker.values())
    chart.add_series("series-B", Faker.values())
    return chart

def line_base() -> Line:
    chart = Line("Line-基本示例", width="100%")
    chart.set_options(labels=["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"],
                      x_label="I'm xlabel",
                      y_label="I'm ylabel")
    chart.add_series("series-A", [57, 134, 137, 129, 145, 60, 49])
    chart.add_series("series-B", [114, 55, 27, 101, 125, 27, 105])
    return chart

def scatter_base() -> Scatter:
    chart = Scatter("Scatter-基本示例")
    chart.set_options(x_label="I'm xlabel", y_label="I'm ylabel")
    chart.add_series("series-A", [(z[0], z[1]) for z in zip(Faker.values(), Faker.values())])
    chart.add_series("series-B", [(z[0], z[1]) for z in zip(Faker.values(), Faker.values())])
    return chart

def main():
    page = Page()
    page.add(pie_base(), radar_base(), line_base(), bar_base(), scatter_base())
    put_html(page.render_notebook())

if __name__ == '__main__':
    start_server(main, debug=True, port=8080)