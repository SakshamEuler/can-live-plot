import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import random
import time
from flask import request
import numpy as np

x_data = [0]
y_data = [0]
x_data_2 = [0]
y_data_2 = [0]
ounter = 0

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-plot'),
    dcc.Interval(
        id='graph-update',
        interval=500,  # Update the graph every 1 second (adjust as needed)
        n_intervals=0
    ),
    dcc.Graph(id='live-plot-2'),
    dcc.Interval(
        id='graph-update-2',
        interval=500,  # Update the graph every 1 second (adjust as needed)
        n_intervals=0
    )
])

@app.callback(
    dash.dependencies.Output('live-plot', 'figure'),
    dash.dependencies.Input('graph-update', 'n_intervals')
)
def update_graph(n):
    global x_data, y_data, ounter
    x_data = list(np.arange(len(y_data)))
    if len(x_data) > 200:
        x_data.pop(0)
        y_data.pop(0)

    # print(y_data)
    # if len(x_data) > 0 and len(y_data) > 0:
    return {'data': [go.Scatter(x=x_data, y=y_data, mode='lines')],
            'layout': go.Layout(xaxis=dict(range=[min(x_data), max(x_data)]),
                                yaxis=dict(range=[0.9*min(y_data), 1.1*max(y_data)]))}
@app.callback(
    dash.dependencies.Output('live-plot-2', 'figure'),
    dash.dependencies.Input('graph-update-2', 'n_intervals')
)
def update_graph_2(n):
    global x_data_2, y_data__2, ounter
    x_data_2 = list(np.arange(len(y_data_2)))
    if len(x_data_2) > 200:
        x_data_2.pop(0)
        y_data_2.pop(0)

    return {'data': [go.Scatter(x=x_data_2, y=y_data_2, mode='lines')],
            'layout': go.Layout(xaxis=dict(range=[min(x_data_2), max(x_data_2)]),
                                yaxis=dict(range=[0.9*min(y_data_2), 1.1*max(y_data_2)]))}


@app.server.route('/update-graph', methods=['POST'])
def update_graph_endpoint():
    global y_data_2
    data = request.args.get('Data')
    y_data.append(float(data))
    return {'message': 'Graph updated successfully'}

@app.server.route('/update-graph-2', methods=['POST'])
def update_graph_endpoint_2():
    global y_data_2
    data = request.args.get('Data')
    y_data_2.append(float(data))
    return {'message': 'Graph updated successfully'}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
