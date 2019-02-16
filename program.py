import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py


file_path = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'polldata_2002_to_2017.csv')
df = pd.read_csv(file_path, encoding='latin1', index_col='Team')  # Deal with San Jose accent mark & set teams as index

file_path2 = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'team_data.csv')
team_data = pd.read_csv(file_path2, encoding='latin1', index_col='School')

weeks = df.loc['Absolute_Week',:].values #Get X-values from data

available_teams = df.index.unique().values[2:] #Get list of teams, throwing away the "Week" and "Absolute_Week" rows

years={
    2002: '2002',
    2003: '2003',
    2004: '2004',
    2005: '2005',
    2006: '2006',
    2007: '2007',
    2008: '2008',
    2009: '2009',
    2010: '2010',
    2011: '2011',
    2012: '2012',
    2013: '2013',
    2014: '2014',
    2015: '2015',
    2016: '2016',
    2017: '2017'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='team_name',
            options=[{'label': i, 'value': i} for i in available_teams],
            value=['Virginia'],  # Default values for team selector
            placeholder='Select a team...',
            multi=True
        )
    ],
    style={'margin': 'auto', 'width': '45%', 'padding': '20px'}), #Center at top of screen

    dcc.Graph(id='poll-graph'),

    html.Div([
        dcc.RangeSlider(
            id='year-selector',
            min=2002,
            max=2017,
            marks=years,
            value=[2002, 2017],
            step=None
            ),
        ],
        style={'margin': 'auto', 'width': '70%', 'padding': '20px'})

])

@app.callback(
    dash.dependencies.Output('poll-graph','figure'),
    [dash.dependencies.Input('team_name','value'),
     dash.dependencies.Input('year-selector', 'value')]
)
def update_graph(team_name, year_selector):

    dff = get_year_limited_data(year_selector)  # Limit data by year

    data = []
    for name in team_name:
        data.append(
            go.Scatter(
                x=dff.loc['Absolute_Week',:].values,
                y=dff.loc[name, :],
                name=name,
                mode='lines',
                line=dict(
                    color=team_data.loc[name, 'Primary Color'],
                    width=4
                ),
                hoverlabel=dict(
                     bgcolor='#FFFFFF'
                 )
            )
        )
    return {
        #'data': data,
        'layout': go.Layout(
            title='Coaches Poll Data',
            xaxis=dict(
                title='Week',
                tickmode='array',
                tickvals=dff.loc['Absolute_Week',:].values,
                ticktext=dff.loc['Week',:].values,
                showgrid=False,
                showticklabels=tick_labels_shown(year_selector)

            ),
            yaxis={'title': 'Votes in the Coaches Poll'},
            shapes=draw_shading(dff.loc['Week',:].values, dff.loc['Absolute_Week',:].values), #Creates the dicts for each shaded rectangle
            annotations=generate_annotations(year_selector, dff.loc['Week',:].values, dff.loc['Absolute_Week',:].values)
        ),
        'data' : data
    }


def get_year_limited_data(year_selector): #Takes a range of dates and returns a modified dataframe with that date range
    list_of_dfs = []
    start_year = year_selector[0]

    while start_year <= year_selector[-1]: #This returns a list of dataframes for each year
        list_of_dfs.append(df.filter(like=str(start_year)))
        start_year = start_year + 1

    return pd.concat(list_of_dfs, axis=1) #return a concatenated dataframe


def draw_shading(relative_week_values, absolute_week_values):
    fill_color = '#d3d3d3'
    opacity = 0.2
    type = 'rect'
    rectangles = []
    shade = True
    previous_week = 0

    for relative_week, absolute_week in zip(relative_week_values, absolute_week_values):

        if relative_week < previous_week and shade: #Create shade block when the weeks roll over
            rectangles.append(dict(type=type, xref='x', yref='paper', x0=str(absolute_week - previous_week - .5), y0='0',
                                   x1=str(absolute_week - .5), y1='1', fillcolor=fill_color, opacity=opacity, layer = 'below',
                                   line=dict(width=0)))
        if absolute_week == absolute_week_values[-1] and shade: #If last shade block
             rectangles.append(dict(type=type, xref='x', yref='paper', x0=str(absolute_week - previous_week - .5), y0='0',
                                    x1=str(absolute_week), y1='1', fillcolor=fill_color, opacity=opacity, layer = 'below',
                                    line=dict(width=0)))
        if relative_week == 1: #Alternate shadyness
            shade = not shade

        previous_week = relative_week

    return rectangles

def generate_annotations(year_range, relative_week_values, absolute_week_values): #Takes week and year data and prints year above each shaded block
    annotations = []
    previous_week = 0
    current_year = 0

    for relative_week, absolute_week in zip(relative_week_values, absolute_week_values):

        if relative_week < previous_week:  # Create annotation over shade block when the weeks roll over
            x_position = absolute_week - previous_week/2
            annotations.append(dict(
                x=x_position,
                y=1.1,
                showarrow=False,
                text=str(year_range[0] + current_year),
                xref='x',
                yref='paper',
                font=dict(
                    size=15,
                    color='#d3d3d3'
                )
            ))
            current_year += 1

        if absolute_week == absolute_week_values[-1]:  # If last block
            x_position = absolute_week - previous_week / 2
            annotations.append(dict(
                x=x_position,
                y=1.1,
                showarrow=False,
                text=str(year_range[0] + current_year),
                xref='x',
                yref='paper',
                font=dict(
                    size=15,
                    color='#d3d3d3'
                )
            ))

        previous_week = relative_week

    return annotations


def tick_labels_shown(years):  # returns a true value if the year range is 4 years or less. This is done so that the week labels don't overlap each other.
    show_ticks = False
    number_of_years = years[-1] - years[0] + 1
    if number_of_years <= 4:
        show_ticks = True

    return show_ticks


if __name__ == '__main__':
    app.run_server(debug=True)

    # [{
    #     'type': 'rect',
    #     'xref': 'x',
    #     'yref': 'y',
    #     'x0': '1',
    #     'y0': '0',
    #     'x1': '10',
    #     'y1': '1000',
    #     'fillcolor': '#d3d3d3',
    #     'opacity': 0.2,
    #     'line': {
    #         'width': 0
    #     }
    # }]