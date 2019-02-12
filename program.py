import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

file_path = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'polldata_2015_to_2017.csv')
df = pd.read_csv(file_path, encoding='latin1', index_col='Team')  # Deal with San Jose accent mark & set teams as index

file_path2 = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'team_data.csv')
team_data = pd.read_csv(file_path2, encoding='latin1', index_col='School')

# dff = df.filter(like='2016')
# print(dff)
# dff2 = df.filter(like='2017')
# print(dff2)
# result = pd.concat([dff,dff2], axis=1)
# print(result)

weeks = df.loc['Absolute_Week',:].values #Get X-values from data

available_teams = df.index.unique().values[2:] #Get list of teams, throwing away the "Week" and "Absolute_Week" rows

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='team_name',
            options=[{'label': i, 'value': i} for i in available_teams],
            value=['Virginia'],
            placeholder='Select a team...',
            multi=True
        )
    ],
    style={'margin': 'auto', 'width': '45%', 'padding': '20px'}), #Center at top of screen

    dcc.Graph(id='poll-graph'),

    html.Div([
        dcc.RangeSlider(
            id='year-selector',
            min=2015,
            max=2017,
            marks={
                2015: '2015',
                2016: '2016',
                2017: '2017'
            },
            value=[2015,2017],
            step=None
            ),
        ],
        style={'margin': 'auto', 'width': '30%', 'padding': '20px'})

])

@app.callback(
    dash.dependencies.Output('poll-graph','figure'),
    [dash.dependencies.Input('team_name','value'),
     dash.dependencies.Input('year-selector', 'value')]
)
def update_graph(team_name, year_selector):
    # dff = []
    # for year in year_selector

    dff = get_year_limited_data(year_selector)

    data = []
    for name in team_name:
        data.append(
            go.Scatter(
                x=weeks,
                y=df.loc[name, :],
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
        'data': data,
        'layout': go.Layout(
            title='Coaches Poll Data',
            xaxis={'title': 'Week'},
            yaxis={'title': 'Votes in the Coaches Poll'}
        )
    }

def get_year_limited_data(year_selector):
    list_of_dfs = []
    start_year = year_selector[0]

    while start_year <= year_selector[-1]: #This returns a list of dataframes for each year
        list_of_dfs.append(df.filter(like=str(start_year)))
        start_year = start_year + 1

    return pd.concat(list_of_dfs, axis=1) #return a concatenated dataframe


if __name__ == '__main__':
    app.run_server(debug=True)