from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

####################################################
# Data treament

df = pd.read_csv('data/dataset_part_2.csv')
df['Class'] = df['Class'].astype('category')

launch_sites = list(df['LaunchSite'].unique())
ls_options = [{'label': 'All sites', 'value': 'All sites'}]
for site in launch_sites:
    ls_options.append({'label': site, 'value': site})

####################################################

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(
        'SpaceX dash app',
        style={'textAlign': 'center'}
    ),

    html.P('Please select a launch site:'),
    
    dcc.Dropdown(
        id='ls_dropdown',
        options=ls_options,
        searchable=False,
        value='All sites'
    ),
    
    html.Br(),

    html.Div(dcc.Graph(id='pie_chart')),
    
    html.Br(),

    html.Div(dcc.Graph(id='scatter_chart')),

    dcc.RangeSlider(
        id='slider',
        min=0,
        max=10000,
        step=1000,
        marks={i:f'{i} KG' for i in range(0, 10000, 1000)},
        value=[0, 10000]
    ),
])

@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='ls_dropdown', component_property='value'),
)
def update_graph(launch_site):

    global df

    if (launch_site == 'All sites') or launch_site == None:

        df0 = df[df['Class'] == 1]
        fig = px.pie(
            df0, 
            names='LaunchSite',
            title='Succeded launches - All sites')
    else:
        
        df0 = df[df['LaunchSite'] == launch_site]
        fig = px.pie(
            df0, 
            names='Class',
            title=f'Succeded launches - {launch_site}')
        
    return fig

@app.callback(
    Output(component_id='scatter_chart', component_property='figure'),    
    Input(component_id='ls_dropdown', component_property='value'),
    Input(component_id='slider', component_property='value'),
)
def update_scattergraph(launch_site, payload):

    global df

    if launch_site == 'All sites' or launch_site == None:
        
        l, h = payload 
        df0 = df[(df['PayloadMass'] > l) & (df['PayloadMass'] < h)]
        fig = px.scatter(
            df0, 
            x='PayloadMass', 
            y='Class',
            color='Class',
            hover_data=['PayloadMass'],
            title=f'Launches by payload mass - All sites')
    else:

        l, h = payload
        df0  = df[(df['LaunchSite'] == launch_site) & (df['PayloadMass'] > l) & (df['PayloadMass'] < h)]
        fig = px.scatter(
            df0, 
            x='PayloadMass', 
            y='Class',
            hover_data=['PayloadMass'],
            title=f'Launches by payload mass - {launch_site}')
        
    return fig
    

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)