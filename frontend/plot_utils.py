from plotly import graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

URL_MAPPING = {'Adilabad': 'https://www.aqi.in/dashboard/india/telangana/adilabad',
               'Nizamabad': 'https://www.aqi.in/dashboard/india/telangana/nizamabad',
               'Khammam': 'https://www.aqi.in/dashboard/india/telangana/khammam',
               'Warangal': 'https://www.aqi.in/dashboard/india/telangana/warangal',
               'Karimnagar': 'https://www.aqi.in/dashboard/india/telangana/karimnagar'
               }
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


def gauge_chart(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [None, 500]},
               'borderwidth': 2,
               'bordercolor': "gray",
               'bgcolor': "white",
               'steps': [
            {'range': [0, 50], 'color': "green"},
            {'range': [51, 100], 'color': "lightgreen"},
            {'range': [101, 200], 'color': "yellow"},
            {'range': [201, 300], 'color': "orange"},
            {'range': [301, 400], 'color': "red"},
            {'range': [401, 500], 'color': "darkred"}
        ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': value}
        },
        title={'text': "AQI levels"}))
    fig.update_layout(font={'color': "darkblue", 'family': "Arial"})

    return fig

def heat_map_chart(df, title):
    df_corr = df.corr()
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            x=df_corr.columns,
            y=df_corr.index,
            z=np.array(df_corr),
            text=df_corr.values,
            texttemplate='%{text:.2f}'
        )
    )
    fig.layout.update(title_text=title)
    return fig


def linechart_with_range_slider(X_axis, Y_axis, parameter_name, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_axis, y=Y_axis,
                  name=parameter_name, line_color="blue"))
    fig.layout.update(title_text=title, xaxis_rangeslider_visible=True)
    return fig


def get_initial():
    URL = "https://aqi-heatwave-app.azurewebsites.net/api/aqi/DailyAQIPredictions/Warangal"
    resp = requests.get(URL)
    return


def get_current_aqi(city):
    global URL_MAPPING, HEADERS
    req = Request(URL_MAPPING[city], headers=HEADERS)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    aqi_val = soup.find('table', {"id": "state-table"})
    table_col, table_data = aqi_val.find('thead'),  aqi_val.find('tbody')
    table_data = table_data.find_all('td')
    table_col = table_col.find_all('th')[1:]
    for val in zip(table_col, table_data):
        name, value = val
        name, value = name.get_text().strip(), value.get_text().strip()
        value = value.replace(",", '')
        if name == 'AQI-IN':
            return (value)


def get_request_data(url, cityname):
    payload = {
        "City": cityname
    }

    r1 = requests.post(url, json=payload)
    data1 = json.loads(r1.text)
    df_fut = json_normalize(data1)
    return df_fut


def bargraph(x_data, y_data1, y_data1_name, xaxis_title, yaxis_title, y_data2=None, y_data2_name=None):
    """
    """
    if y_data2 == None and y_data2_name == None:
        fig = go.Figure(data=[
            go.Bar(name=y_data1_name, x=x_data,
                   y=y_data1, marker_color='crimson'),
        ])
    else:
        fig = go.Figure(data=[
            go.Bar(name=y_data1_name, x=x_data,
                   y=y_data1, marker_color='crimson'),
            go.Bar(name=y_data2_name, x=x_data, y=y_data2, marker_color='navy')
        ])

    fig.update_layout(xaxis_title=xaxis_title,
                      yaxis_title=yaxis_title, barmode='group')
    return fig


def linegraph(x_data, y_data1, y_data1_name, xaxis_title, yaxis_title, y_data2=None, y_data2_name=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data1, name=y_data1_name))
    if y_data2_name != None:
        fig.add_trace(go.Scatter(x=x_data, y=y_data2,
                                 name=y_data2_name, marker_color='crimson'))
    fig.update_layout(
        xaxis_title=xaxis_title, yaxis_title=yaxis_title, font=dict(color="white"))
    return fig
