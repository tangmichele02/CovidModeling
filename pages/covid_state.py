import requests
import json
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
from datetime import date
import plotly.express as px
import plotly.graph_objs as go
# import geopandas
import streamlit as st 
# import geopy
import plotly.figure_factory as ff

state = "WA"

def get_state_data(state): 
    """
    makes api query to COVID Act Now for individual state data 

    param state (str): relevant state

    return: (dict) json of state data 
    """
    response_state_timeseries = requests.get(f"https://api.covidactnow.org/v2/county/{state}.json?apiKey={apiKey}")

    # checks access
    if response_state_timeseries.status_code == 200:
        data_timeseries = response_state_timeseries.json()
        return data_timeseries

data_timeseries_state = get_state_data(state)
print(data_timeseries_state)
fips = []
vals = []
for val in data_timeseries_state: 
    fips.append(val["fips"])
    vals.append(val["hsaPopulation"])

fig = ff.create_choropleth(fips=fips, values=vals)
fig.layout.template = None
fig.show()


# references: 
# https://medium.com/@arun_prakash/mastering-apis-and-json-with-python-2685dfb0a115
# https://www.section.io/engineering-education/missing-values-in-time-series/
# https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
# https://medium.com/nerd-for-tech/how-to-plot-timeseries-data-in-python-and-plotly-1382d205cc2
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
# https://discuss.streamlit.io/t/datetime-slider/163/12
# https://www.geeksforgeeks.org/creating-a-list-of-range-of-dates-in-python/
# https://plotly.com/python/figure-labels/
# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
# https://www.digitalocean.com/community/tutorials/python-string-to-datetime-strptime
# https://plotly.com/python/graph-objects/
