"commandline: panel serve app.py --dev"


import hvplot.pandas
import numpy as np
import pandas as pd
import panel as pn
import seaborn as sns
from configparser import ConfigParser


# for the design
PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

pn.extension(design="material", sizing_mode="stretch_width")


@pn.cache
def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config


config = read_config("config.ini")
# mulecules_file = config['FILES']['molecules']
data_path = config['FILES']['data']


def get_data():
    return pd.read_csv(data_path, header=0)


def widgets(data):
    histogram_variable = pn.widgets.Select(
        name="variable", options=list(data.columns))
    return histogram_variable


# ! x =histogram_variable, maar koppeling werkt nog niet
def plot_body(data, histogram_variable):
    histogram_body = sns.displot(data, x="SCOR_VAL", stat="percent",
                                 kde=True, color="blue", hue="DEPRESSION_T1")
    return histogram_body


def main():
    data = get_data()
    histogram_variable = widgets(data)
    histogram_body = plot_body(data, histogram_variable)

    pn.template.MaterialTemplate(
        site="Panel",
        title="test",
        sidebar=[histogram_variable],
        main=[histogram_body]).servable()


main()
