"commandline: panel serve app.py --dev"

from configparser import ConfigParser
import pandas as pd
import panel as pn
import hvplot.pandas


pn.extension(design = "material", sizing_mode = "stretch_width")


@pn.cache
def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config


config = read_config("config.ini")
data_path = config['FILES']['data']
# height = config['SETTINGS']["height"]  # hoe werkend maken met getal ?
height = 350
width = 350

def get_data():
    return pd.read_csv(data_path, header = 0)


# gesorteerde lists voor de inpput oties van de gebruiker
def lists():
    var_list = ('BIRTHYEAR', 'AGE_T1', 'AGE_T2', 'AGE_T3', 'ZIP_CODE',
       'BMI_T1', 'WEIGHT_T1', 'HIP_T1', 'HEIGHT_T1', 'WAIST_T1', 'BMI_T2',
       'WEIGHT_T2', 'HIP_T2', 'HEIGHT_T2', 'WAIST_T2', 'HEIGHT_T3',
       'WEIGHT_T3', 'HIP_T3', 'WAIST_T3', 'FINANCE_T1', 'DBP_T1', 'DBP_T2',
       'HBF_T1', 'HBF_T2', 'MAP_T1', 'MAP_T2', 'SBP_T1', 'SBP_T2', 'CHO_T1',
       'GLU_T1', 'CHO_T2', 'GLU_T2', 'LLDS', 'SUMOFALCOHOL', 'SUMOFKCAL', 'MWK_VAL',
       'SCOR_VAL', 'MWK_NO_VAL', 'SCOR_NO_VAL', 'PREGNANCIES', 'C_SUM_T1', 'A_SUM_T1',
       'SC_SUM_T1', 'I_SUM_T1', 'E_SUM_T1', 'SD_SUM_T1', 'V_SUM_T1',
       'D_SUM_T1', 'NSES_YEAR', 'NSES', 'NEIGHBOURHOOD1_T2', 'NEIGHBOURHOOD2_T2',
       'NEIGHBOURHOOD3_T2', 'NEIGHBOURHOOD4_T2', 'NEIGHBOURHOOD5_T2',
       'NEIGHBOURHOOD6_T2', 'MENTAL_DISORDER_T1', 'MENTAL_DISORDER_T2')
    groupby_list = ('GENDER','EDUCATION_LOWER_T1',
       'EDUCATION_LOWER_T2', 'WORK_T1', 'WORK_T2',
       'LOW_QUALITY_OF_LIFE_T1', 'LOW_QUALITY_OF_LIFE_T2',
       'HTN_MED_T1', 'RESPIRATORY_DISEASE_T1', 'SMOKING', 'METABOLIC_DISORDER_T1',
       'METABOLIC_DISORDER_T2', 'SPORTS_T1',
       'CYCLE_COMMUTE_T1', 'VOLUNTEER_T1', 'OSTEOARTHRITIS',
       'BURNOUT_T1', 'DEPRESSION_T1', 'SLEEP_QUALITY', 'DIAG_CFS_CDC',
       'DIAG_FIBROMYALGIA_ACR', 'DIAG_IBS_ROME3', 'NEIGHBOURHOOD1_T2', 'NEIGHBOURHOOD2_T2',
       'NEIGHBOURHOOD3_T2', 'NEIGHBOURHOOD4_T2', 'NEIGHBOURHOOD5_T2',
       'NEIGHBOURHOOD6_T2', 'MENTAL_DISORDER_T1', 'MENTAL_DISORDER_T2')
    return var_list, groupby_list
# bug: 'NEIGHBOURHOOD1_T2' --> legenda niet volledig in beeld
# bug: scatterplot --> sorteert de legenda niet op volgorde


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
    widget_scatter_second = pn.widgets.Select(name = 'Selectie y-as',
                                             options = list(var_list))
    widget_scatter_first = pn.widgets.Select(name = 'Selectie x-as',
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
    data = get_data()
    var_list, groupby_list = lists()
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


    metadata = "!PLACEHOLDER VOOR WELKOM EN METADATA"

    # the site build together
    template = pn.template.MaterialTemplate(
        site="LifeLines",
        title="",
        main = pn.Tabs(("Informatiepunt", metadata), ("scatterplot",scatter), ("Histogram", hist)))
    template.servable()


main()
