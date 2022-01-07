# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
#test
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

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

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
)
error_count = 1
ip_count = 13
delay_count = 3.2

hdd = dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                    350, 430, 474, 526, 488, 537, 500, 439],
                    name='* of Disk use',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Disk',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )
bp = dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                    350, 430, 474, 526, 488, 537, 500, 439],
                    name='% of BP use',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Bandwith',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )
cpu = dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                    299, 340, 403, 549, 499],
                    name='% of CPU use',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='CPU',
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
                    html.Span(className="number-field", id="live_error"),
                    html.Span(className="number-type", children="Erreurs")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'green'}, children=[
                    html.Span(className="number-field", children=ip_count),
                    html.Span(className="number-type", children="Adresses IP uniques")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=[
                    html.Span(className="number-field", children=delay_count),
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
                            style={'height': 300},
                            id='cpu'
                        )
                    ])
                )),
                html.Div(className="col-sm number-data", style={'color': 'green'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = bp,
                            style={'height': 300},
                            id='bp'
                        )
                    ])
                )),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = hdd,
                            style={'height': 300},
                            id='hdd'
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
        interval=5*1000, # in milliseconds
        n_intervals=0
    )
])
@app.callback(Output('live_error', 'children'),
              Input('interval-component', 'n_intervals'))
def update_error(input_value):
    return format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
