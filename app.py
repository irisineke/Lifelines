"commandline: panel serve app.py --dev"

from configparser import ConfigParser
# import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import matplotlib.pyplot as plt
import hvplot.pandas


# for the design
PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

pn.extension(design = "material", sizing_mode = "stretch_width")


@pn.cache
def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config


config = read_config("config.ini")
data_path = config['FILES']['data']


def get_data():
    return pd.read_csv(data_path, header = 0)


# def widgets(data):
#     histogram_variable = pn.widgets.Select(
#         name="variable", options=list(data.columns))
#     return histogram_variable


def widget_hist(data):
    widget_hist_multi = pn.widgets.MultiChoice(
        name = 'Histogram', options = list(data.columns))
    return widget_hist_multi


# def histplot_body(data, histogram_variable):
#     histogram_body = data.hvplot.scatter(y=histogram_variable, bins=50,
#                                          alpha=0.5, height=400)
#     return histogram_body


def histplot_body(data, widget_hist_multi):
    histplot = data.hvplot.hist(y = widget_hist_multi, bins = 50,
                                     alpha = 0.5, height = 400)
    return histplot


def widget_scatter(data):
    widget_scatter_first = pn.widgets.Select(
        name = 'Scatterplot_first', options = list(data.columns))

    widget_scatter_second = pn.widgets.Select(
        name = 'Scatterplot_second', options = list(data.columns))
    return widget_scatter_first, widget_scatter_second


def scatterplot_body(data, widget_scatter_first, widget_scatter_second):
    scatterplot = data.hvplot.scatter(y = widget_scatter_first, x = widget_scatter_second, by = "DEPRESSION_T1")
    return scatterplot


def main():
    data = get_data()
    # histogram_variable = widgets(data)
    widget_hist_multi = widget_hist(data)
    widget_scatter_first, widget_scatter_second = widget_scatter(data)

    # histogram = pn.bind(histplot_body, data, histogram_variable)
    histogram = pn.bind(histplot_body, data, widget_hist_multi)
    scatterplot = pn.bind(scatterplot_body, data, widget_scatter_first, widget_scatter_second)

    # the site build together
    pn.template.MaterialTemplate(
        site="LifeLines",
        title="Depressie",
        sidebar=[widget_scatter_first, widget_scatter_second, widget_hist_multi],
        main=[scatterplot, histogram]).servable()


main()
