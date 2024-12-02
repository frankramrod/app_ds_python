# Import required libraries
import pandas as pd
import numpy as np
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

df = pd.read_csv('spacex_launch_dash.csv')

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36',
            'font-size': 40}),
# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)
    html.Div([
        html.H2('Select launch site from dropdown'),
        dcc.Dropdown(
            id='site-dropdown',
            options=['All'] + list(df['Launch Site'].unique()),
            placeholder='Select launch site',
            value='All',
            searchable=True)
        ]),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    html.Div([
        html.H2('Select payload range from slider'),
            dcc.RangeSlider(
                id='payload-slider',
                min=df['Payload Mass (kg)'].min(),
                max=df['Payload Mass (kg)'].max(),
                step=1000,
                value=[df['Payload Mass (kg)'].min(),
                    df['Payload Mass (kg)'].max()]
            )
        ]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(input_site_dropdown):

    if input_site_dropdown == 'All':
        fig = px.pie(
            data_frame=df,
            values='class',
            names='Launch Site',
            title='Ratio of success launches by site'
        )

        return fig

    else:
        filterd_df = df[df['Launch Site'] == input_site_dropdown]
        total = filterd_df.shape[0]
        success = filterd_df['class'].sum()
        failed = total - success

        dict_values = {'outcome': ['Failed','Success'],
            'values': [failed,success]}

        selected_df = pd.DataFrame(dict_values)

        fig = px.pie(
            data_frame=selected_df,
            values='values',
            names='outcome',
            title=f'Sucess-Failed of success launches at {input_site_dropdown}'
        )

        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_plot(input_site_dropdown,input_payload_slider):

    if input_site_dropdown == 'All':

        range=((input_payload_slider[0] < df['Payload Mass (kg)']) &
            (df['Payload Mass (kg)'] < input_payload_slider[1]))

        print(range)

        narrow_df = df[range]

        figure = px.scatter(
            data_frame=narrow_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Launch success by payload mass and booster category'
        )

        return figure

    else:
        filterd_df = df[df['Launch Site'] == input_site_dropdown]

        range = ((input_payload_slider[0] < filterd_df['Payload Mass (kg)']) &
            (filterd_df['Payload Mass (kg)'] < input_payload_slider[1]))

        narrow_df = filterd_df[range]

        figure = px.scatter(
            data_frame=narrow_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Launch success by payload mass and booster category at {input_site_dropdown}'
        )

        return figure


# Run the app

#port = np.random.randint(low=1000, high=9999).__str__()
#print(port)

if __name__ == '__main__':
    app.run_server(debug=True) #, port=port
