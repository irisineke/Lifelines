"commandline: panel serve app.py --dev"

from configparser import ConfigParser
# import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import matplotlib.pyplot as plt
import hvplot.pandas


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


def widget_hist(data):
    widget_hist_multi = pn.widgets.MultiChoice(
        name = 'Histogram', options = list(data.columns))
    return widget_hist_multi


def histplot_body(data, widget_hist_multi):
    histplot = data.hvplot.hist(y = widget_hist_multi, bins = 50,
                                     alpha = 0.5, height = 400)
    return histplot


def widget_scatter(data):
    widget_scatter_first = pn.widgets.Select(name = 'Scatterplot_y', 
                                             options = list(data.columns))
    widget_scatter_second = pn.widgets.Select(name = 'Scatterplot_x', 
                                              options = list(data.columns))
    return widget_scatter_first, widget_scatter_second


def scatterplot_body(data, widget_scatter_first, widget_scatter_second):
    scatterplot = data.hvplot.scatter(y = widget_scatter_first, 
                                      x = widget_scatter_second, 
                                      by = "DEPRESSION_T1")
    return scatterplot


def main():
    data = get_data()
    widget_hist_multi = widget_hist(data)
    widget_scatter_first, widget_scatter_second = widget_scatter(data)

    histogram = pn.bind(histplot_body, data, widget_hist_multi)
    scatterplot = pn.bind(scatterplot_body, data, widget_scatter_first, widget_scatter_second)

    # layout tryout
    # row1 = pn.Row(sidebar = [widget_scatter_first, widget_scatter_second],
    #               main = [scatterplot])
    # row2 = pn.Row(sidebar2 = [widget_hist_multi],
    #               main = [histogram])


    # the site build together
    template = pn.template.MaterialTemplate(
        site="LifeLines",
        title="Depressie",
        # sidebar = [widget_scatter_first, widget_scatter_second, widget_hist_multi],
        # main = [scatterplot, histogram]
    )

    # the layout
    template.main.append(
        pn.Card(
            pn.Row(
                pn.Card(widget_scatter_first, widget_scatter_second),
                pn.Card(scatterplot))))

    template.main.append(
        pn.Card(
            pn.Row(
                pn.Card(widget_hist_multi),
                pn.Card(histogram)))
    )


    template.servable()


main()
