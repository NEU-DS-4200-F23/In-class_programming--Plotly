# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # In-Class Programming—Plotly

# %% [markdown]
# # 911-call activity
#
# This data is from Montgomery County, Pennsylvania, and available via [Kaggle](https://www.kaggle.com/datasets/mchirico/montcoalert/data).
#
# In this kernel, we will Analyze and Visualize the 911 calls data based on different variables.

# %%
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime as dt

# %%
data = pd.read_csv('911.csv')
data

# %%
data.isnull().sum()

# %% [markdown]
# Lets leave zip for now we will only use it for the top 10 zip codes for most number of 911 calls.
#
# First, let's drop null townships.

# %%
data.dropna(subset=['twp'], inplace=True)

# %%
data.isnull().sum()

# %%
data['timeStamp'].head(3)

# %% [markdown]
# Our column 'timeStamp' is in string format and hence we must convert it to 'Datetime' format.

# %%
data['timeStamp'] = pd.to_datetime(data['timeStamp'])

# %%
data['timeStamp'].head(3)

# %%
data['year'] = data['timeStamp'].dt.year

# %% [markdown]
# Adding one column to our data : 'reason_cat' for the category of reason. This will enable us to better understand and visualize the dataset.

# %%
data['reason_cat'] = data['title'].apply(lambda x: x.split(':')[0])
data['reason_cat'].unique()

# %% [markdown]
# #### Different Reasons to call 911?

# %%
reason = data.groupby(['reason_cat']).size().reset_index()
reason.columns = ['reason', 'count']
reason

# %%
# Bar Chart
fig1 = px.bar(
    reason,
    x='reason',
    y='count',
    color_discrete_sequence=[px.colors.qualitative.Pastel],
    text='count',
    title='Category of Reasons for 911 Calls'
)

fig1.update_layout(
    xaxis_title='Reason Category',
    xaxis={'categoryorder':'total descending'},
    yaxis_title='Count',
    showlegend=False,
    template='ggplot2')

fig1.show()

# %%
# Pie Chart
fig2 = px.pie(
    reason, 
    values='count',
    names='reason',
    title='Category of Reasons for 911 Calls',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hole=0.5,
    height=600
)

fig2.update_traces(
    sort=True,
    direction='clockwise',
    textinfo='percent+label', pull=[0, .2, 0])

fig2.data[0].marker.line.width = 2
fig2.data[0].marker.line.color = "black"

fig2.show()

# %% [markdown]
# EMS (Emergency Medical Services) calls are the most frequent.
# Traffic calls are less frequent and Fire calls being the least frequent.

# %% [markdown]
# #### let us look top 10 reasons to call 911

# %%
top_10_reasons = data['title'].value_counts().to_frame(name='count').head(10).sort_values(by='count')
top_10_reasons

# %%
fig3 = px.bar(
    top_10_reasons,
    x='count',
    color_discrete_sequence=[px.colors.qualitative.Pastel],
    orientation='h',
    text='count',
    title='Top 10 Reasons for 911 Calls'
)

fig3.update_layout(
    xaxis_title='Count',
    yaxis_title='Reasons',
    template='plotly_white'
)

fig3.show()

# %% [markdown]
# Approximately 28% of all calls are for vehicle accidents.
# Followed by disabled vehicle calls which constitutes nearly 7% of all calls.

# %% [markdown]
# ### Top 10 townships from 2015-2020 for 911 calls

# %%
years = range(2015, 2021)
titles = ['Top Townships in ' + str(year) for year in years]

fig4 = make_subplots(
    rows=len(years),
    cols=1,
    subplot_titles=(titles))

r = 0
for year in range(2015, 2021):
    r = r+1    
    year_data = data[data['year']==year]
    year_data_twp = year_data['twp'].value_counts().to_frame()
    top_sorted_twp = year_data_twp.head(10).sort_values(by='count')    
    fig4.add_trace(go.Bar(x=top_sorted_twp.index, y=top_sorted_twp['count'], name=year), row=r, col=1)

fig4.update_layout(title_text='Top Townships for 911 Calls', height=1500, template='plotly_white')

fig4.show()

# %% [markdown]
# # Unemployment world-wide

# %% [markdown]
# [Data](https://www.kaggle.com/datasets/sovannt/world-bank-youth-unemployment/data) and [example code](https://www.kaggle.com/code/arthurtok/generation-unemployed-interactive-plotly-visuals) from Kaggle.

# %%
country = pd.read_csv('API_ILO_country_YU.csv')
country.head()

# %%
country['change'] = country['2014'] - country['2010']
country

# %%
px.choropleth(
    country,
    locations='Country Code',
    color='2014',
    hover_name='Country Name',
    height = 600
).show()

# %%
fig = px.choropleth(
    country,
    locations='Country Code',
    color='change',
    hover_name='Country Name',
    color_continuous_scale=px.colors.diverging.PuOr_r,
    height = 600
).show()

# %%
px.choropleth(
    country,
    locations='Country Code',
    color='change',
    hover_name='Country Name',
    color_continuous_scale=px.colors.diverging.PuOr_r,
    height = 600,
    projection = 'orthographic'
).show()

# %%
px.scatter_geo(
    country,
    locations='Country Code',
    color='change',
    hover_name='Country Name',
    size='2014',
    height = 600,
        projection = 'orthographic'

).show()

# %%
