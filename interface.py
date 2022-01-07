# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
from script1 import getData
import numpy

# external JavaScript files
external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        'integrity': 'sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
        'integrity': 'sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    },
    {
        'href': './assets/style.css',
        'rel': 'stylesheet'
    }
]
data = getData("monitorme2.ddns.net", "other_vhosts_access.log")

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
)
error_count = 1
ip_count = 13
delay_count = 3.2

XH = []
XH.append(0)

YH = []
YH.append(0)
hdd = dict(
            data=[
                dict(
                    x=[],
                    y=[],
                    name='% of Disk use',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Disk(%)',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )
X = []
X.append(0)

Y = []
Y.append(0)
cpu = dict(
            data=[
                dict(
                    x=[],
                    y=[],
                    name='% of CPU use',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='CPU(%)',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )

app.layout = html.Div(className="main-container", children=[
    html.Nav(className="navbar navbar-light bg-light", children=[
    html.Div(className='navbar-brand', children=[
        html.H1(className="h1-logo",
            children=[html.Img(className="logo",src='https://www.freeiconspng.com/thumbs/dashboard-icon/dashboard-icon-3.png'),'Dashboard']
        ),
        ])
    ]),
    html.Div(className="container content", children=[
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Données")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=[
                html.Div(className="col-sm number-data", style={'color': 'red'}, children=[
                    html.Span(className="number-field", id="live_error", children=(data[3])),
                    html.Span(className="number-type", children="Erreurs")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'green'}, children=[
                    html.Span(className="number-field", id="live_ip",children=(data[4])),
                    html.Span(className="number-type", children="Adresses IP uniques")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=[
                    html.Span(className="number-field", id="live_delay"),
                    html.Span(className="number-type", children="Délai de réponse (en us)")
                ])
                ])
                )
            )]
        ),
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Données")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=[
                html.Div(className="col-sm number-data", style={'color': 'red'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = cpu,
                            style={'height': 400},
                            id='cpu',
                            animate=True
                        )
                    ])
                )),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = hdd,
                            style={'height': 400},
                            id='hdd',
                            animate=True
                        )
                    ])
                ))
                ])
                )
            )]
        ),
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Pages visitées")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=(
                    html.Table(className="table", style={"textAlign": "center"},children=[
                        html.Thead(children=(
                            html.Tr(children=[
                                html.Th(children=("Page")),
                                html.Th(children=("Nombre de visites"))
                            ])
                        )),
                        html.Tbody(children=[
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ]),
                            html.Tr(children=[
                                html.Td(children=("/index.html")),
                                html.Td(children=("3"))
                            ])
                        ])
                    ])
                ))
                )
            )]
        ),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=30*1000, # in milliseconds
        n_intervals=0
    )
])
@app.callback(
    Output('live_error', 'children'),
    Output('live_ip', 'children'),
    Output('cpu', 'figure'),
    Output('hdd', 'figure'),
    Input('interval-component', 'n_intervals'))
def callback(n):
    data = getData("monitorme2.ddns.net", "other_vhosts_access.log")
    X.append(n)
    Y.append(data[0])
    data_c = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name="* of CPU use",
        mode='lines+markers'
    )
    XH.append(n)
    YH.append(data[1])
    data_h = plotly.graph_objs.Scatter(
        x=list(XH),
        y=list(YH),
        name="% of Disk use",
        mode='lines+markers'
    )
    data_cpu = {'data': [data_c],
                'layout':go.Layout(xaxis=dict(range=[0,max(X)]),yaxis=dict(range=[numpy.amin(numpy.array(Y).astype(float)),numpy.amax(numpy.array(Y).astype(float))]))}
    data_hdd = {'data': [data_h],
                'layout':go.Layout(xaxis=dict(range=[0,max(XH)]),yaxis=dict(range=[numpy.amin(numpy.array(YH).astype(float)),numpy.amax(numpy.array(YH).astype(float))]))}

    return data[3], data[4], data_cpu, data_hdd

if __name__ == '__main__':
    app.run_server(debug=True)
