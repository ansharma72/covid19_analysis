# Check option to build maps using folium or leaflet

# Common Libraries includes packages like
#        numpy for linear algebra
#        pandas for data processing and file I/O
#        urllib for url based access to data
#        request.utils for formatting URIs

import numpy as np
import pandas as pd
import urllib.request as url_req
from requests.utils import requote_uri

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Common global functions used across the code base

############## Global Functions Start ################################
# transpose data from a specific column
def transform_data(df=None, name=None):
    return df[df['Country/Region'] == name].iloc[:, 4:].T


# Read data from the url encoded by converting the url to standard format
# ensuring that it is fully and consistently quoted.
#    url   : The url to visit
def read_encoded_data(url=None):
    url_who_table = requote_uri(url)
    with url_req.urlopen(url_who_table) as response:
        data = response.read()
    return data

# Read data in csv format from the url specified
#  url   : The url to visit
#  print : control debug output
def read_csv(url, print=False):
    if len(url) == 0:
        print("URL is missing")
        exit()
    data = pd.read_csv(url)
    if (print):
        data.head()
    return data


############## Global Functions Ends ################################

# get covid-19 global data
global_covid_19_data = read_csv("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")
print(" The columns in the data are : ", global_covid_19_data.columns)

# Snapshot extracted from John hopkins into data folder :
raw_confirmed = pd.read_csv('../data/RAW_global_confirmed_cases.csv')
raw_deaths = pd.read_csv('../data/RAW_global_deaths.csv')

print("The raw data with confirmed :", raw_confirmed.head())

# Transpose data from colnum 4 onwards
us = transform_data(df=raw_confirmed, name='US')
print(us.head(5))

us_conf = pd.read_csv('../data/RAW_us_confirmed_cases.csv')
us_death = pd.read_csv('../data/RAW_us_deaths.csv')
us_meta = pd.read_csv('../data/CONVENIENT_us_metadata.csv')

us = transform_data(df=raw_confirmed, name='US')
us.columns = ['confirmed']
us['deaths'] = transform_data(df=raw_deaths, name='US').values
print(us.tail())

# Insight 1 : Shows the rise of Covid infection in USA

# Display the graph of infections in USA related to COVID
us_infections = us.plot(y='confirmed', title='USA Covid-19 spreading')
plt.show()

# Display the graph of deaths in USA related to COVID
us_fig_deaths = us.plot(y='deaths', title='USA Covid-19 spreading')
plt.show()

# TBD - Combine into a single map
# fig, axs = plt.subplots(2)
# fig.suptitle('US Infections and deaths')
# axs[0].plot(x='',y='confirmed', title='USA Covid-19 spreading')
# axs[1].plot(x='', y='deaths', title='USA Covid-19 spreading')

# Insight 2 : Shows the rise of Covid infection in Ireland
ireland_infected = raw_confirmed[raw_confirmed['Country/Region'] == 'Ireland']
ireland_death = raw_deaths[raw_deaths['Country/Region'] == 'Ireland']
print(ireland_infected.head())
print(ireland_death.head())

import plotly.express as px

ireland_last_day = ireland_infected.iloc[:, -1].name

uk_fig = px.scatter_mapbox(ireland_infected, lat=ireland_infected.Lat, lon=ireland_infected.Long, color=ireland_last_day,
                           size=ireland_last_day, hover_name='Country/Region', zoom=8,
                           mapbox_style='open-street-map', title='Confirmed cases Covid-19 Ireland and ROW map.')
uk_fig.show()

# Insight 3 - Load Ireland specific data


# Insight 4 -

# Insight 5

# Insight 5
