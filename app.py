'''
Author: Iris Ineke
Date: 22 januari 2025
Versie: 1

Dit script maakt een website waarin je variabelen kunt kiezen
om een scatterplot en/of histogram te maken.

Voorbeeld om te runnen:
panel serve app.py --dev
'''

from configparser import ConfigParser
import ast
import pandas as pd
import panel as pn
import hvplot.pandas


pn.extension(design = "material", sizing_mode = "stretch_width")


@pn.cache
def read_config():
    '''
    Deze functie leest het config file in.
    : return, data, string met pad naar de data
    : return, metadata, string met pad naar de metadata
    : return, height, int met hoogte plots
    : return, width, int met breedte plots
    : return, var_list, list met kolomnamen voor variable
    : return, groupby, list met kolomnamen voor groupby
    '''
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
    '''
    Inlezen data.
    : return, data, dataframe met de data
    '''
    return pd.read_csv(data, header = 0)


def get_metadata(metadata):
    '''
    Inlezen metadata.
    : return, metadata, tabel met de metadata
    '''
    return pd.read_csv(metadata, sep=';', header=None, names=["Naam", "Betekenis"])


def widget_hist(var_list, groupby_list):
    '''
    Maakt de widget aan voor de histogram. Slaat op wat wordt geselecteerd door de gebruiker.
    : param, var_list, list met kolomnamen voor variable
    : param, groupby, list met kolomnamen voor groupby
    : return, widget_hist_var, een select met de gekozen variabele
    : return, widget_groupby_hist, een select met de gekozen groupby
    '''
    widget_hist_var = pn.widgets.Select(
        name = 'Selectie gegevens', options = list(var_list))
    widget_groupby_hist = pn.widgets.Select(
        name = 'Sorteren op', options = list(groupby_list))
    widget_scat_switch = pn.widgets.Switch(name='Subplots', width = 50)
    return widget_hist_var, widget_groupby_hist, widget_scat_switch


def histplot_body(data, widget_hist_var, widget_groupby_hist, widget_scat_switch):
    '''
    Maakt de histogram aan met de ingevulde variabelen.
    : param, data, dataframe met de data
    : param, widget_hist_var, een select met de gekozen variabele
    : param, widget_groupby_hist, een select met de gekozen groupby
    : return, histplot, een histogram van de ingevulde variabele
    '''
    histplot = data.hvplot.hist(y = widget_hist_var, by = widget_groupby_hist, subplots = widget_scat_switch)
    return histplot


def widget_scatter(var_list, groupby_list):
    '''
    Maakt de widget aan voor de scatterplot. Slaat op wat wordt geselecteerd door de gebruiker.
    : param, var_list, list met kolomnamen voor variable
    : param, groupby, list met kolomnamen voor groupby
    : return, widget_scatter_first, een select met de gekozen variabele voor de y-as
    : return, widget_scatter_second, een select met de gekozen variabele voor de x-as
    : return, widget_groupby_scat, een select met de gekozen groupby
    '''
    widget_scatter_first = pn.widgets.Select(name = 'Selectie Y-as',
                                             options = list(var_list))
    widget_scatter_second = pn.widgets.Select(name = 'Selectie X-as',
                                             options = list(var_list))
    widget_groupby_scat = pn.widgets.Select(name = 'Sorteren op',
                                            options = list(groupby_list))
    switch_button = pn.widgets.Checkbox(name = 'Wissel assen')
    print(type(switch_button))
    # return widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button
    return widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button



def scatterplot_body(data, widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button):
    '''
    Maakt de scatterplot aan met de ingevulde variabelen.
    : param, data, dataframe met de data
    : param, widget_scatter_first, een select met de gekozen variabele voor de y-as
    : param, widget_scatter_second, een select met de gekozen variabele voor de x-as
    : param, widget_groupby_scat, een select met de gekozen groupby
    : return, scatterplot, een scatterplot van de ingevulde variabele
    '''
    if switch_button == True:
        print('HEY HIJ IS TRUE!!')
        first_value = widget_scatter_first
        second_value = widget_scatter_second
        widget_scatter_first = second_value
        widget_scatter_second = first_value
        # switch_button = False


    # if switch_button == False:
    #     print('HEY HIJ IS FALSE!!')

    scatterplot = data.hvplot.scatter(y = widget_scatter_first,
                                      x = widget_scatter_second,
                                      by = widget_groupby_scat)

    return scatterplot


def main():
    '''
    Bindt alle functies aan elkaar.
    '''
    data, metadata, height, width, var_list, groupby_list = read_config()
    data = get_data(data)
    metadata = get_metadata(metadata)
    widget_hist_var, widget_groupby_hist, widget_scat_switch = widget_hist(var_list, groupby_list)
    widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button = widget_scatter(var_list,
                                                                                      groupby_list)

    histogram = pn.bind(histplot_body, data, widget_hist_var, widget_groupby_hist, widget_scat_switch)
    scatterplot = pn.bind(scatterplot_body, data,
                          widget_scatter_first, widget_scatter_second, widget_groupby_scat, switch_button)


    # de verschillende tabs aangemaakt:
    scatter = pn.Row(
        pn.Card(widget_scatter_first, switch_button, widget_scatter_second, widget_groupby_scat,
                title = "Instellingen", height = height, width = width),
        pn.Card(scatterplot, title = "Scatterplot", height = height))


    hist = pn.Column(
        pn.Card(widget_hist_var, widget_groupby_hist, pn.pane.Markdown('Verdeel in subplots:', height = 25), widget_scat_switch, title = "Instellingen"),
        pn.Card(histogram, title = "Histogram"))


    # the site samengevoegd
    template = pn.template.MaterialTemplate(
        site="LifeLines",
        title="",
        main = pn.Tabs(("scatterplot",scatter), ("Histogram", hist), ("Informatiepunt", metadata)))
    template.servable()


main()
