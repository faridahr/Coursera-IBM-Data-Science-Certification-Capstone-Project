# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print("Max Payload:", max_payload)
print("Min Payload:", min_payload)
# Create a dash application
app = dash.Dash(__name__)
site_list = list(spacex_df['Launch Site'].unique())
#state_dict = dict(site_list : site_list)
#print(site_list)
#print(type(site_list))
#site_list.append('All Sites')
#site_list.append('ALL')

OptionList = [{'label': site, 'value': site} for site in site_list]
OptionList.insert(0,{'label': 'All Sites', 'value': 'ALL'})

# {'label': site, 'value': site} for site in site_list
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                    dcc.Dropdown(id='site-dropdown',
                options=OptionList,
                value='ALL',
                placeholder="Select site(s)",
                searchable=True
                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2500: '100',
                       5000: '500',
                       7500: '1000',
                       10000: '10000'},
                value=[min_payload, max_payload]),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    #print("Entered Site: ", entered_site)
    if entered_site == 'ALL':
        
        filtered_df = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        #print(filtered_df)
        #print(type(filtered_df))
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='title')
       # print(fig)
        return fig
    else:
        filtered_df1 = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class')['class'].count().reset_index(name = 'count')
       # fig = px.pie(spacex_df[spacex_df['Launch Site'] == entered_site], values='class', 
        fig = px.pie(filtered_df1, values='count',
        names='class', 
        title='title')
        #print(fig)
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site1, entered_payload):
    filtered_df1 = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    print("Entered Site: ", entered_site1, "Entered Payload:", entered_payload)
    if entered_site1 == 'ALL':
        filtered_df1 = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
        #filtered_df = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        #print(filtered_df)
        #print(type(filtered_df))
        fig1 = px.scatter(filtered_df1, x = 'Payload Mass (kg)', y = 'class', color="Booster Version Category")
        return fig1
    else:
        filtered_df1 = filtered_df1[filtered_df1['Launch Site'] == entered_site1]
        fig1 = px.scatter(filtered_df1, x = 'Payload Mass (kg)', y = 'class', color="Booster Version Category")
        return fig1
# Run the app
if __name__ == '__main__':
    app.run_server()