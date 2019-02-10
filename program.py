import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

file_path = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'polldata_2017.csv')
df = pd.read_csv(file_path, encoding='latin1', index_col='Team')  # Deal with San Jose accent mark & set teams as index

file_path2 = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'team_data.csv')
team_data = pd.read_csv(file_path2, encoding='latin1', index_col='School')

weeks = []
for week in df:
    weeks.append(int(week)) # This function gets the # of weeks in each dataset (basically, the x-axis)

available_teams = df.index.unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='team_name',
            options=[{'label': i, 'value': i} for i in available_teams],
            value=['Virginia'],
            multi=True
        )
    ],
    style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='poll-graph')

])

@app.callback(
    dash.dependencies.Output('poll-graph','figure'),
    [dash.dependencies.Input('team_name','value')]
)
def update_graph(team_name):
    data = []
    for name in team_name:
        data.append(
            go.Scatter(
                x=weeks,
                y=df.loc[name, :],
                name=name,
                line=dict(
                    color=team_data.loc[name, 'Primary Color'],
                    width=4
                )
            )
        )
    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'Week'},
            yaxis={'title': 'Votes in the Coaches Poll'}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)