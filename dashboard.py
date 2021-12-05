import pathlib
import os
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = Dash(__name__, url_base_pathname='/dashboard/')
server = app.server

#Loading the data and cleaning it
app_path = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(app_path, os.path.join("data", "HomeC.csv")))
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

theme = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#title page
def build_banner():
    return html.Div(
        className='col-sm-10 row banner',
        children=[
            html.Div(
                className='banner-text',
                children=[
                    html.H5('Enegry Consumed by Specific Appliances'),
                ],
            ),
        ],
    )

app.layout = html.Div(
    className='big-app-container',
    children=[
        build_banner(),
        html.Div(children='''
        Graphics for the energy consumed by appliances
        '''),
        dcc.Dropdown(id="my_dropdown",
                 options=[
                     {"label": "Dishwasher", "value": 'dishwasher_[kw]'},
                     {"label": "Fridge", "value": 'fridge_[kw]'},
                     {"label": "Garage Door", "value": 'garage_door_[kw]'},
                     {"label": "Microwave", "value": 'microwave_[kw]'},
                     ],
                 multi=False,
                 value = 'dishwasher_[kw]',
                 style={'width': "40%"}
                 ),
        html.Br(),
        html.Br(),
        html.Div(id='output_container', children=[]),
        html.Br(),
        dcc.Graph(id='my_graph', figure={}),
    ]
)
my_dict = {'dishwasher_[kw]':"Dishwasher", 'fridge_[kw]':"Fridge", 
            'garage_door_[kw]':"Garage Door", 'microwave_[kw]':"Microwave"}
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_graph', component_property='figure')],
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_graph(option_slctd):
    container = "The appliance chosen was: {}".format(my_dict[option_slctd])
    figure={
        'data': 
        [
            {
                'x': df['time'][:500],
                'y': df[option_slctd][:500],
                'name': option_slctd,
                'marker': {'size': 12}
            },
        ],
        'layout': 
        {
            'plot_bgcolor': theme['background'],
            'paper_bgcolor': theme['background'],
            'font': {
                'color': theme['text']
            },
            'xaxis':{
                'title':'Time'
            },
            'yaxis':{
                'title':'Energy Consumed in Kw'
            }
        }
    }
    return container, figure