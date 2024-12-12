# def widgets(data):
#     histogram_variable = pn.widgets.Select(
#         name="variable", options=list(data.columns))
#     return histogram_variable


# def histplot_body(data, histogram_variable):
#     histogram_body = data.hvplot.scatter(y=histogram_variable, bins=50,
#                                          alpha=0.5, height=400)
#     return histogram_body



# main:
    # histogram_variable = widgets(data)
    # histogram = pn.bind(histplot_body, data, histogram_variable)