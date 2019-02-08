# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 22:16:30 2018

@author: Baoyp
"""
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State, Event

app = dash.Dash(__name__)
server = app.server
app.title = 'Airbnb Recommendation'
app.config['suppress_callback_exceptions']=True

# API keys and datasets
mapbox_access_token = 'pk.eyJ1IjoicXVpbm50YW5nIiwiYSI6ImNqcDdocjZqdzFwZWYzd25yZXNranI5YnEifQ.hL-fy1TBtR0j0ai_dFLF0w'
#map_data = pd.read_csv("nyc-wi-fi-hotspot-locations.csv")
df = pd.read_csv('database_2.csv')
df = df.drop('Unnamed: 0',axis=1)

# Selecting only required columns
#map_data = map_data[["Borough", "Type", "Provider", "Name", "Location", "Latitude", "Longitude"]].drop_duplicates()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#ff5a5f"),
    titlefont=dict(color="#ff5a5f", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
   hovermode="closest",
   plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='💡 Exciting Housing You May Interest In',
    style={'color': '#ff5a5f','font':'Bello'},
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)

# functions
def gen_map(df):
   # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(df['latitude']),
                "lon": list(df['longtitude']),
                "hoverinfo": "text",
                "hovertext": [["Housing ID: {} <br>Housing Url: {}".format(i,j)]
                                for i,j in zip(df['listing_id'], df['listing_url'])],
                "mode": "markers",
                "name": list(df['listing_id']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }

app.layout = html.Div(    
    html.Div(style={'background-image':'https://cdn-images-1.medium.com/max/2000/1*i0X-WUnBqi60fzsMPxsxZQ.png'},children=[
        html.Div(
            [   html.H1(children='Airbnb The One Just For You', 
                        style={'color': '#ff5a5f','font':'Bello','Bold':'True'},
                        className='nine columns'),
                html.Img(
                    src=#"https://www.proactive.marketing/wp-content/uploads/2014/07/New-airbnb-logo-jpg-resized-600.png",
                    #'https://media1.tenor.com/images/f41eedf4cc4be29995b4f77dcf3534ed/tenor.gif?itemid=4896074',
                    #'https://editorial.designtaxi.com/editorial-images/news-SamaraAirbnb040816/2-Airbnb-Debuts-inhouse-designstudio-samara-brand-logo-identity-design.gif',
                    'https://media.giphy.com/media/3oEduINJ2NotvNYOf6/giphy.gif',
                    className='three columns',
                    style={
                        'height': '20%',
                        'width': '20%',
                        'float': 'right',
                        'position': 'relative',
                        'padding-top': 12,
                        'padding-right': 0
                    },
                ),
                html.Img(
                    src="https://cdn-images-1.medium.com/max/2000/1*i0X-WUnBqi60fzsMPxsxZQ.png",
                    className='three columns',
                    style={
                        'height': '100%',
                        'width': '100%',
                        'float': 'center',
                        'position': 'relative',
                        'padding':'10'
                    },
                ),
                html.Div(children='''
                        🏘️ Pick your favourite Airbnb in New York City Right Now!
                        ''',
                        style={'color': '#ff5a5f', 'font':'Bello','fontSize': 25,'Bold':'True'},
                        className='nine columns'
                )
            ], className="row"
        ),
    
    
        # Selectors
        html.Div(
            [
                html.Div(
                    [
                        html.P('🗺️ Choose Borroughs:',
                               style={'color': '#ff5a5f','font':'Bello','fontsize':'20'}),
                        dcc.Dropdown(
                                id = 'borough',
                                options=[{'label':i, 'value':i} for i in df['neighbourhood_group'].unique()],
                                value='Manhattan',
                                
                                #labelStyle={'display': 'inline-block'}
                        ),
                        
                        html.P('',style={'padding':'10'}),
                        
                        html.P('💰 Price Level:',
                               style={'color': '#ff5a5f','font':'Bello','fontsize':'20'}),
                        dcc.RangeSlider(
                                id='pricelevel',
                                min=0,
                                max=500,
                                step=50,
                                value=[50, 100],
                                marks={
                                        0: '0',
                                        100: '$100',
                                        200: '$200',
                                        300: '$300',
                                        400: '$400',
                                        500: '$500'
                                        }
                                ),
                        
                        html.P('',style={'padding':'10'}),
                        
                        html.P('🛏️ Choose Number of Bedrooms:',
                               style={'color': '#ff5a5f','font':'Bello','fontsize':'20'}),
                        dcc.Dropdown(
                                id = 'numbed',
                                options=[{'label': 'Studio', 'value': 0},
                                         {'label': 1, 'value': 1},
                                         {'label': 2, 'value': 2},
                                         {'label': 3, 'value': 3},
                                         {'label': 4, 'value': 4},
                                         {'label': 5, 'value': 5},
                                         {'label': 6, 'value': 6},
                                         {'label': 7, 'value': 7},
                                         {'label': 8, 'value': 8}],
                                         value=[0, 1],
                                         multi=True
                                         ),
                        html.P('',style={'padding':'10'}),
                        
                        html.P('🛀 Choose Number of Bathrooms',
                               style={'color': '#ff5a5f','font':'Bello','fontsize':'20'}),
                        dcc.Dropdown(
                                id = 'numbath',
                                options=[{'label': 0, 'value': 0},
                                         {'label': 1, 'value': 1},
                                         {'label': 2, 'value': 2},
                                         {'label': 3, 'value': 3},
                                         {'label': 4, 'value': 4},
                                         {'label': 5, 'value': 5},
                                         {'label': 6, 'value': 6},
                                         {'label': 7, 'value': 7},
                                         {'label': 16, 'value': 16}],
                                         value=[0, 1],
                                         multi=True
                                         ),
                        html.P('',style={'padding':'10'}),
                        
                        html.P('🚶‍ Love to Walk?',
                               style={'color': '#ff5a5f','font':'Bello','fontsize':'20'}),
                        html.Label("📍 Choose how far you'd like to walk ",
                                   style={'color': '#ff5a5f','font':'Bello','fontsize':'15'}),
                        dcc.Slider(
                                id='max_dist',
                                min=0,
                                max=2,
                                step=0.5,
                                value=0,
                                marks={
                                        0: '0',
                                        0.5: '0.5 miles',
                                        1: '1 miles',
                                        1.5: '1.5 miles',
                                        2: '2 miles'})
                            
                    ],
                    className='six columns',
                    style={'margin-top': '20','padding-right':'30',
                        'width': '49%','display': 'inline-block'}
                ),
                        
                html.Div(id='intermediate-value', style={'display': 'none'}),
                
                html.Div(
                    [
                            html.P('😄 Choose Your Preference',
                            style={'color': '#ff5a5f','font':'Bello','fontsize':'20','Bold':'True'}),
                                   
                     html.P('❓ 0 for least importmant 😒, 5 for most important 😊',
                            style={'color': '#ff5a5f','font':'Bello','fontsize':'5','padding':'5'}),
        
                     html.P('🚩 Customer Experience',
                            style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                     dcc.Slider(
                             id='customer_experience',
                             min=0,
                             max=5,
                             step=0.5,
                             marks={
                                     0: '0',
                                     1: '1',
                                     2: '2',
                                     3: '3',
                                     4: '4',
                                     5: '5'},
                                     value=2.5,
                                     ),
                    html.P('',style={'padding':'10'}),
                    
                    html.P('🍽️ Catering Accessibility',
                           style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                    dcc.Slider(
                            id='num_restaurant',
                            min=0,
                            max=5,
                            step=0.5,
                            marks={
                                    0: '0',
                                    1: '1',
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5'},
                                    value=2.5,
                                    ),
                    html.P('',style={'padding':'10'}),     
                    
                    html.P('🚇 Subway Accessibility',
                           style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                    dcc.Slider(
                            id='dist_closest_subway',
                            min=0,
                            max=5,
                            step=0.5,
                            marks={
                                    0: '0',
                                    1: '1',
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5'},
                                    value=2.5,
                                    ),
                    html.P('',style={'padding':'10'}),
                    
                    html.P('🚌 Bus Accessibility',
                           style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                    dcc.Slider(
                            id='dist_closest_bus',
                            min=0,
                            max=5,
                            step=0.5,
                            marks={
                                    0: '0',
                                    1: '1',
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5'},
                                    value=2.5,
                                    ),
                    html.P('',style={'padding':'10'}),
                    
                    html.P('💧 Cleaniness',
                           style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                    dcc.Slider(
                            id='review_score_cleaniness',
                            min=0,
                            max=5,
                            step=0.5,
                            marks={
                                    0: '0',
                                    1: '1',
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5'},
                                    value=2.5,
                                    ),
                    html.P('',style={'padding':'10'}),
                    
                    html.P('💌 Host Evaluation',
                           style={'color': '#ff5a5f','font':'Bello','fontsize':'10'}),
                    dcc.Slider(
                            id='host_related',
                            min=0,
                            max=5,
                            step=0.5,
                            marks={
                                    0: '0',
                                    1: '1',
                                    2: '2',
                                    3: '3',
                                    4: '4',
                                    5: '5'},
                                    value=2.5,
                                    ),
                    html.P('',style={'padding':'10'}),
                            ],
                    className='six columns',
                    style={'margin-top': '20','padding-left':'30','width':'49%','display': 'inline-block'}
                )
            ],
            className='row'
        ),

        # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dt.DataTable(
                            rows=df.to_dict('records'),
                            columns=['listing_id','listing_url','Score'],
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            selected_row_indices=[],
                            id='datatable'),
                    ],
                    style = layout_table,
                    className="six columns"
                ),
            ], className="row"
        ),                      
    ],
    className='ten columns offset-by-one')
    )                       

#改到这里了！！！
@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
                    
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)


###Test
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('borough', 'value'),
     Input('pricelevel', 'value'),
     Input('numbed', 'value'),
     Input('numbath', 'value'),
     Input('max_dist', 'value')])
def update_selected_row_indices(borough,pricelevel,numbed,numbath,max_dist):
    dff = df[(df['neighbourhood_group']==borough) & (df['price']>=pricelevel[0]) 
    & (df['price']<=pricelevel[1]) & (df['bedrooms'].isin(numbed)) & (df['bathrooms'].isin(numbath)) 
    & (df['dis_to_closest_bus']<max_dist) 
    & (df['dis_to_closest_subway']<max_dist)]#[['listing_id','listing_url']]
    
    #rows1 = dff.to_dict('records')
    return dff.to_json(date_format='iso', orient='split')

@app.callback(
    Output('datatable', 'rows'),
    [Input('intermediate-value', 'children'),
     Input('customer_experience','value'),
     Input('num_restaurant','value'),
     Input('dist_closest_subway','value'),
     Input('dist_closest_bus','value'),
     Input('review_score_cleaniness','value'),
     Input('host_related','value')])
def updated_selected_row_scores(jsonified_selected_data,customer_experience,
                                num_restaurant,dist_closest_subway,dist_closest_bus,
                                review_score_cleaniness,host_related):
    df2 = pd.read_json(jsonified_selected_data, orient='split')
    df2['Score'] = customer_experience*df2['customer_experience'] + num_restaurant*df2['num_restaurant']
    + dist_closest_subway * df2['dis_to_closest_subway']+ dist_closest_bus*df2['dis_to_closest_bus']
    +review_score_cleaniness*df2['review_scores_cleanliness']
    + host_related*(df2['review_scores_communication']+df2['review_scores_checkin'])/2
    
    rows = df2.to_dict('records')
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)