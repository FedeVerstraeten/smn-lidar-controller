# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import pandas as pd
import numpy as np
import json

app = Dash(__name__)

# json data
lidar_json = None 
path_json = './json/'
file_json = 'lidar_20220520_223218.json'
with open(path_json + file_json) as file:
  lidar_json = json.load(file)

# lidar config
limit_init = 100 # meters
limit_final = 3000 # meters

BIN_METERS = 7.5
bin_init = int(limit_init/BIN_METERS)
bin_final = int(limit_final/BIN_METERS)

range_meters = np.arange(limit_init,limit_final,BIN_METERS)

# create data frame
df = pd.DataFrame({'meters':range_meters})

for i in lidar_json:
  tr='TR' + str(i)
  other=pd.DataFrame({
            tr:lidar_json[i]["data_mv"][bin_init:bin_final]
            })
  df=df.join(other)

df.index = df['meters']

# making plots
fig = go.Figure()
fig = make_subplots()

# Adding traces
for col in df.columns[1:]: 
  fig.add_trace(
    go.Scatter(
      x=df.index,
      y=df[col],
      name=col,
      text=df[col],
      mode="lines",
      # marker_color='#39ac39',
      opacity=1
    ),
    secondary_y=False
  )

# Add figure title
fig.update_layout(legend=dict(
  orientation="h",
  yanchor="bottom",
  y=1.02,
  xanchor="right",
  x=0.93),
  title={
  'text': '<span style="font-size: 20px;">Multiple LiDAR signal </span><br><span style="font-size: 10px;">(click and drag)</span>',
  'y': 0.97,
  'x': 0.45,
  'xanchor': 'center',
  'yanchor': 'top'},
  paper_bgcolor="#ffffff",
  plot_bgcolor="#ffffff",
  width=1200, height=500
)


# Set axes titles
fig.update_xaxes(rangeslider_visible=False,title_text="Height [m]")
fig.update_yaxes(title_text="Raw LiDAR signals [mV]",)

# fig.update_layout(width=1200, height=500)

# web app config with Dash
app.layout = html.Div(children=[
  html.H1(children='Lidar signals with Dash'),

  html.Div(children='''
    Dash: A web application framework for your data.
  '''),

  dcc.Graph(
    id='example-graph',
    figure=fig
  )
])

# Running server localhost
if __name__ == '__main__':
  app.run_server(debug=True)