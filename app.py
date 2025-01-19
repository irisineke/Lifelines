"commandline: panel serve app.py --dev"

from configparser import ConfigParser
import ast
import pandas as pd
import panel as pn
import hvplot.pandas


pn.extension(design = "material", sizing_mode = "stretch_width")


@pn.cache
def read_config():
    config = ConfigParser()
    config.read('config.ini')

    data = config['FILES']['data']
    metadata = config['FILES']['metadata']
    height = int(config['SETTINGS']['height'])
    width = int(config['SETTINGS']['width'])
    var_list = ast.literal_eval(config['SETTINGS']['var_list'])
    groupby_list = ast.literal_eval(config['SETTINGS']['groupby_list'])
    return data, metadata, height, width, var_list, groupby_list


def get_data(data):
    return pd.read_csv(data, header = 0)


def get_metadata(metadata):
    return pd.read_csv(metadata, sep=';', header=None, names=["Naam", "Betekenis"])


def widget_hist(var_list, groupby_list):
    widget_hist_var = pn.widgets.Select(
        name = 'Selectie gegevens', options = list(var_list))
    widget_groupby_hist = pn.widgets.Select(
        name = 'Sorteren op', options = list(groupby_list))
    return widget_hist_var, widget_groupby_hist


def histplot_body(data, widget_hist_var, widget_groupby_hist):
    histplot = data.hvplot.hist(y = widget_hist_var, by = widget_groupby_hist)
    return histplot


def widget_scatter(var_list, groupby_list):
    widget_scatter_first = pn.widgets.Select(name = 'Selectie Y-as',
                                             options = list(var_list))
    widget_scatter_second = pn.widgets.Select(name = 'Selectie X-as',
                                             options = list(var_list))
    widget_groupby_scat = pn.widgets.Select(name = 'Sorteren op',
                                            options = list(groupby_list))
    return widget_scatter_first, widget_scatter_second, widget_groupby_scat


def scatterplot_body(data, widget_scatter_first, widget_scatter_second, widget_groupby_scat):
    scatterplot = data.hvplot.scatter(y = widget_scatter_first,
                                      x = widget_scatter_second,
                                      by = widget_groupby_scat)
    return scatterplot


def main():
    data, metadata, height, width, var_list, groupby_list = read_config()
    data = get_data(data)
    metadata = get_metadata(metadata)
    widget_hist_var, widget_groupby_hist = widget_hist(var_list, groupby_list)
    widget_scatter_first, widget_scatter_second, widget_groupby_scat = widget_scatter(var_list,
                                                                                      groupby_list)

    histogram = pn.bind(histplot_body, data, widget_hist_var, widget_groupby_hist)
    scatterplot = pn.bind(scatterplot_body, data,
                          widget_scatter_first, widget_scatter_second, widget_groupby_scat)


    # the verschillende tabs:
    scatter = pn.Row(
        pn.Card(widget_scatter_first, widget_scatter_second, widget_groupby_scat,
                title = "Instellingen", height = height, width = width),
        pn.Card(scatterplot, title = "Scatterplot", height = height))


    hist = pn.Row(
        pn.Card(widget_hist_var, widget_groupby_hist, title = "Instellingen",
                height = height, width = width),
        pn.Card(histogram, title = "Histogram", height = height))


    # the site build together
    template = pn.template.MaterialTemplate(
        site="LifeLines",
        title="",
        main = pn.Tabs(("scatterplot",scatter), ("Histogram", hist), ("Informatiepunt", metadata)))
    template.servable()


main()
