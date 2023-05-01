import requests
import json
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
from datetime import date
import plotly.express as px
import streamlit as st 

apiKey = st.secrets["apiKey"]
state = "WA"

def get_state_data(state): 
    """
    makes api query to COVID Act Now for individual state data 

    param state (str): relevant state

    return: (dict) json of state data 
    """
    response_state_timeseries = requests.get(f"https://api.covidactnow.org/v2/county/{state}.timeseries.json?apiKey={apiKey}")

    # checks access
    if response_state_timeseries.status_code == 200:
        data_timeseries = response_state_timeseries.json()
        return data_timeseries

def dev_data(data_timeseries, date):

    fips_vals = []
    cases = []
    deaths = []
    for val in data_timeseries: 
        if val["lastUpdatedDate"] == date:
            fips_vals.append(val["fips"])
            cases.append(val["actuals"]["cases"])
            deaths.append(val["actuals"]["deaths"])
            
    df = pd.DataFrame(list(zip(fips_vals, cases, deaths)),
                  columns = ["fips", "cases", "deaths"])
    return df 

def make_graph(df): 

    with open('./pages/geojson-counties-fips.json', 'r') as response:
        counties = json.load(response)

    fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale="Viridis",
                           scope = "usa",
                           labels={'cases':'Cases'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def get_dates(): 
    """
    makes datetime objects for first day and today's date 

    return: (tuple) start date and end date as datetime objects 
    """
    start_date = date(2020, 3, 9)  #  I need some range in the past
    end_date = date(2023, 4, 23)
    # end_date = dt.now().date()
    return (start_date, end_date)


def get_num_days(): 
    """
    gets total number of days between start date and end date

    return: (int) total number of days between start date and end date 
    """
    start_date, end_date = get_dates()
    max_days = end_date-start_date
    max_days_int = max_days.days
    return max_days_int


def make_date_range():
    """
    creates list of dates (as strings) for selector bar 

    return: (list of str) list of dates 
    """
    date_range = []

    start_date = get_dates()[0]
    max_days_int = get_num_days()

    for day in range(max_days_int + 1):
        date_val = (start_date + timedelta(days = day)).strftime("%b %d, %Y")
        date_range.append(date_val)

    return date_range




def main(): 

    cols1,_ = st.columns((8,4)) 

    dates = get_dates()

    with st.sidebar:

        date_sel = st.slider(
            label = "Select a date",
            min_value = dates[0], 
            max_value = dates[-1]
        )

        state_option = st.selectbox(
            "Select State",
            ("AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", 
             "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
             "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "NE", "NH",
             "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", 
             "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WI", "WV", "WY"
             )
        )
    
    # date_object = dt.strptime(date_sel, "%b %d, %Y")
    new_date_str = date_sel.strftime("%Y-%m-%d")
    st.write(new_date_str)
    state_data_timeseries = get_state_data(state_option)
    df = dev_data(state_data_timeseries, "2023-04-30")

    st.plotly_chart(make_graph(df))
    st.write("Cases Table")
    st.dataframe(df)

main()

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

# downloaded geo-json-counties-fips.json from https://github.com/plotly/datasets/blob/master/geojson-counties-fips.json
