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
from scipy import stats
from matplotlib import rcParams

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

# Get COVID-19 global data from WHO
global_covid_19_data = read_csv("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")
print(" The columns in the data are : ", global_covid_19_data.columns)

# Snapshot extracted from John hopkins into data folder
raw_confirmed = pd.read_csv('../data/RAW_global_confirmed_cases.csv')
raw_deaths    = pd.read_csv('../data/RAW_global_deaths.csv')
print("The raw data with confirmed :", raw_confirmed.head())

us_conf = pd.read_csv('../data/RAW_us_confirmed_cases.csv')
us_death = pd.read_csv('../data/RAW_us_deaths.csv')
us_meta = pd.read_csv('../data/CONVENIENT_us_metadata.csv')

# Filter 2 data columns - confirmed infection(confirmed) and deaths(deaths) for US for the timeline
us = transform_data(df=raw_confirmed, name='US')
us.columns = ['confirmed']
us['deaths'] = transform_data(df=raw_deaths, name='US').values
print(us.tail())

# Insight 1 : Plot the rise of Covid infection in USA and the associated deaths in US
plt.style.use('seaborn-white')
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,10), gridspec_kw={'height_ratios': [1, 2]})
fig.suptitle('Infections and deaths in USA')
us["confirmed"].plot( y='confirmed', title='Covid-19 spreading in USA', ax=ax1)
us["deaths"].plot( y='deaths', title='Covid-19 deaths in USA', ax=ax2)
plt.show()

ireland = transform_data(df=raw_confirmed, name='Ireland')
ireland.columns = ['confirmed']
ireland['deaths'] = transform_data(df=raw_deaths, name='Ireland').values
print(ireland.tail())

# Insight 2 : Shows the rise of Covid infection in Ireland
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,10), gridspec_kw={'height_ratios': [1, 2]})
fig.suptitle('Infections and deaths in Ireland')
ireland["confirmed"].plot( y='confirmed', title='Covid-19 spreading in Ireland', ax=ax1)
ireland["deaths"].plot( y='deaths', title='Covid-19 deaths in Ireland', ax=ax2)
plt.show()

# Insight 3 -
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(10,10))

fig.suptitle('Infection and death rates')
axes[0][0].set_title('Ireland Covid Infection')
sns.distplot(x=ireland["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution", ax=axes[0][0])
axes[0][1].set_title("Ireland Covid Deaths")
sns.boxplot(ax=axes[0][1], x=ireland["deaths"])


axes[1][0].set_title('US Covid Infection')
sns.distplot(x=us["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution", ax=axes[1][0])
axes[1][1].set_title("US Covid Deaths")
sns.boxplot(ax=axes[1][1], x=us["deaths"])

plt.show()
#fig, (ax[1][0], ax[1][0], ax[0][0], ax[0][0]) =plt.subplots(nrows=2, ncols=2, figsize=(18,12))
#plt.subplots_adjust(hspace=0.4, top=0.8)

# Loan amount distribution plots

#sns.distplot(us["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution", ax=ax1[0][0])
#sns.boxplot(us["confirmed"], ax=ax2[0][0])
#plt.show()
# bw_adjust controls the smoothing
#sns.displot(x= tmp.loan_amnt, label="Loan Amount Frequency distribution", kind="kde", bw_adjust=4, ax=ax[0][2])
#sns.displot(x= tmp.loan_amnt, label="Loan Amount Frequency distribution", kind="kde", bw_adjust=0.2, ax=ax[0][3])

# Insight 4 - Load Ireland specific data
import plotly.express as px
ireland_infected = raw_confirmed[raw_confirmed['Country/Region'] == 'Ireland']
ireland_death = raw_deaths[raw_deaths['Country/Region'] == 'Ireland']
ireland_last_day = ireland_infected.iloc[:, -1].name

uk_fig = px.scatter_mapbox(ireland_infected, lat=ireland_infected.Lat, lon=ireland_infected.Long, color=ireland_last_day,
                           size=ireland_last_day, hover_name='Country/Region', zoom=8,
                           mapbox_style='open-street-map', title='Confirmed cases Covid-19 Ireland map.')
uk_fig.show()
# Insight 5

