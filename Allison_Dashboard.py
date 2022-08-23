# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)


                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': i, 'value':i} for i in spacex_df['Launch Site'].unique()],
                                value='ALL',
                                placeholder='Select a Launch Site',
                                searchable=True),
                                


                                
html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
#dcc.Graph(id='success-pie-chart'),
html.Br(),
html.Div(dcc.Graph(id='success-pie-chart')),
html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000:'1000', 5000: '5000'},
                                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output('success-pie-chart', 'figure'),
              [Input('site-dropdown', 'value')])

def get_pie_chart(entered_site):
    filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site=='ALL':
        d=spacex_df.groupby('Launch Site')['class'].mean()
        fig=px.pie(d, values='class',
        names=spacex_df['Launch Site'].unique(),
        title='Total Success Launches')
        
        
    else:
        data1=filtered_df['class'].value_counts()
        fig=px.pie(data1, values='class',
        names=filtered_df['class'].unique(),
        title='Total Success Launches for: '+ entered_site)
        
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
              
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def scatter_plot(entered_site, payload):
    
    pld_filter=spacex_df.loc[spacex_df['Payload Mass (kg)'].between(payload[0], payload[1])]
    filtered_df=pld_filter[pld_filter['Launch Site']==entered_site]
    if entered_site=="ALL":
        fig2=px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload versus Launch Outcome')
        
    else:
        fig2=px.scatter(pld_filter, x='Payload Mass (kg)', y='class',color='Booster Version Category', title='Payload versus Launch Outcome for '+ entered_site)

    return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
