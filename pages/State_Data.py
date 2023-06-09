import requests
import json
import pandas as pd
from datetime import timedelta
from datetime import datetime as dt
from datetime import date
import plotly.express as px
import streamlit as st 

# get apiKey from secrets 
apiKey = st.secrets["apiKey"]

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
    """
    gets county data for specific date 

    param data_timeseries (json): state data 
    param date (str): date

    return: (dataframe) dataframe with counties (fips), cases, deaths
    """

    fips_vals = []
    cases = []
    deaths = []

    # loops through counties
    for county in data_timeseries: 

        fips_vals.append(county["fips"])

        # gets timeseries data 
        for val in county["actualsTimeseries"]: 

            if val["date"] == date:
                cases.append(val["cases"])
                deaths.append(val["deaths"])

                # no need to traverse rest of data
                break
            
    df = pd.DataFrame(list(zip(fips_vals, cases, deaths)),
                  columns = ["fips", "Cases", "Deaths"])
    return df 


def make_graph(df, type): 
    """
    creates choropleth map of specific state's covid data 

    param df (dataframe): covid data dataframe
    param type (str): either cases or deaths 

    return: choropleth map 
    """

    # opens geojson file with all fips (similar to zip code), see references for download source
    with open('./pages/geojson-counties-fips.json', 'r') as response:
        counties = json.load(response)

    fig = px.choropleth(df, geojson=counties, locations='fips', color=type,
                           color_continuous_scale="Viridis",
                           scope = "usa",
                           labels={type:type},
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def get_dates(): 
    """
    makes datetime objects for first day and today's date 

    return: (tuple) start date and end date as datetime objects 
    """

    start_date = date(2020, 3, 9)  #  I need some range in the past
    end_date = dt.now().date()
    return (start_date, end_date)


def main(): 
    """
    runs program 
    """

    cols1,_ = st.columns((8,4)) 

    dates = get_dates()

    with st.sidebar:

        date_sel = st.slider(
            label = "Select a date",
            min_value = dates[0], 
            max_value = dates[-1]
        )

        map_option = st.selectbox(
            "Select map type",
            ("Cases", "Deaths")
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
    
    new_date_str = date_sel.strftime("%Y-%m-%d")
    state_data_timeseries = get_state_data(state_option)
    df = dev_data(state_data_timeseries, new_date_str)

    st.title("COVID-19 State Data")
    st.write("**Total " + map_option + " for " + state_option + " on " + new_date_str + "**")
    st.plotly_chart(make_graph(df, map_option))
    st.write("**Cases Table**")
    st.dataframe(df)


main()

# references: 

# downloaded geo-json-counties-fips.json from https://github.com/plotly/datasets/blob/master/geojson-counties-fips.json
