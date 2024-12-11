"commandline: panel serve app.py --dev"


# import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import matplotlib.pyplot as plt
import hvplot.pandas
from configparser import ConfigParser


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
# mulecules_file = config['FILES']['molecules']
data_path = config['FILES']['data']


def get_data():
    return pd.read_csv(data_path, header = 0)


# def widgets(data):
#     histogram_variable = pn.widgets.Select(
#         name="variable", options=list(data.columns))
#     return histogram_variable


def widget_hist(data):
    widget_hist_multi = pn.widgets.MultiChoice(
        name = 'MultiSelect', options = list(data.columns))
    # multi_select_values = multi_select.value
    return widget_hist_multi


# ! x =histogram_variable, maar koppeling werkt nog niet
# def histplot_body(data, histogram_variable):
#     histogram_body = data.hvplot.scatter(y=histogram_variable, bins=50,
#                                          alpha=0.5, height=400)
#     return histogram_body


def histplot_body(data, multi_select):
    histplot_body = data.hvplot.hist(y = multi_select, bins = 50,
                                     alpha = 0.5, height = 400)
    return histplot_body


def main():
    data = get_data()
    # histogram_variable = widgets(data)
    # histogram_body = plot_body(data, histogram_variable)
    widget_hist_multi = widget_hist(data)
    # scatterplot_body(data)

    # histogram = pn.bind(histplot_body, data, histogram_variable)
    scatterplot = pn.bind(histplot_body, data, widget_hist_multi)
    pn.template.MaterialTemplate(
        site="LifeLines",
        title="Depressie",
        sidebar=[widget_hist_multi],
        main=[scatterplot]).servable()


main()
