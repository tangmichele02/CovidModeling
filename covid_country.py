import requests
import json
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
from datetime import date
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st 

apiKey = st.secrets["apiKey"]

def get_country_data(): 
    """
    makes api query to COVID Act Now for United States data

    return: (dict) json of country data 
    """
    response_country_timeseries = requests.get(f"https://api.covidactnow.org/v2/country/US.timeseries.json?apiKey={apiKey}")

    # checks access 
    if response_country_timeseries.status_code == 200: 
        data_timeseries = response_country_timeseries.json()
        return data_timeseries


def dev_data(data_timeseries): 
    """
    creates lists for relevant data (total cases, new cases, total deaths, new deaths) and dates

    return: tuple of lists
    """
    dates = []
    cases_total = []
    cases_new = []
    deaths_new = []
    deaths_total = []

    for vals in data_timeseries["actualsTimeseries"]: 

        date = vals["date"]
        date_object = dt.strptime(date, "%Y-%m-%d")
        dates.append(date_object)

        cases_total.append(vals["cases"])
        cases_new.append(vals["newCases"])
        deaths_total.append(vals["deaths"])
        deaths_new.append(vals["newDeaths"])
    
    return dates, cases_total, cases_new, deaths_total, deaths_new


def cases_fig(title_name, dates, cases, start_date_object, end_date_object): 
    """
    creates plotly graph object for relevant graph and relevant time range

    param title_name (str): graph title
    param dates (list of datetimes): list of all dates 
    param cases (list of int): list of case values
    param start_date_object (datetime): date to start 
    param end_date_object (datetime): date to end 

    return: figure 
    """
    start_index = dates.index(start_date_object)
    end_index = dates.index(end_date_object)

    fig = go.Figure(data = go.Scatter(x = dates[start_index:end_index + 1], y = cases[start_index:end_index + 1]))
    fig.update_layout(title = title_name)
    fig.update_xaxes(title_text = "Date")
    fig.update_yaxes(title_text = "Count")
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
    """
    runs program 
    """
    cols1,_ = st.columns((8,4)) 

    date_range = make_date_range()

    with st.sidebar:

        start_date_sel, end_date_sel = st.select_slider(
            "Select a range of dates",
            options = date_range,
            value = (date_range[0], date_range[-1])
        )

        graph_option = st.selectbox(
            "Select graph type",
            ("All time total cases", "New cases per day", "All time total deaths", "New deaths per day")
        )
    
    start_date_object = dt.strptime(start_date_sel, "%b %d, %Y")
    end_date_object = dt.strptime(end_date_sel, "%b %d, %Y")

    data_timeseries = get_country_data()

    dev_data_output = dev_data(data_timeseries)

    st.title("Country Data")  
    
    if graph_option == "All time total cases":
        st.write(cases_fig("All time total cases", dev_data_output[0], dev_data_output[1], start_date_object, end_date_object))
    elif graph_option == "New cases per day":
        st.write(cases_fig("New cases per day", dev_data_output[0], dev_data_output[2], start_date_object, end_date_object))
    elif graph_option == "All time total deaths":
        st.write(cases_fig("All time total deaths", dev_data_output[0], dev_data_output[3], start_date_object, end_date_object))
    elif graph_option == "New deaths per day":
        st.write(cases_fig("New deaths per day", dev_data_output[0], dev_data_output[4], start_date_object, end_date_object))


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
