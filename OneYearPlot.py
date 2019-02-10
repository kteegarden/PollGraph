# This script plots one year (2017) of data and assigns the correct color to each team

import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

file_path = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'polldata_2017.csv')
df = pd.read_csv(file_path, encoding='latin1')  # Deal with San Jose accent mark & set teams as index

file_path2 = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'team_data.csv')
team_data = pd.read_csv(file_path2, encoding='latin1', index_col='School')

weeks = []
for week in df.iloc[:,1:]:
    weeks.append(int(week)) # This function gets the # of weeks in each dataset (basically, the x-axis)


df['Total Votes'] = df.sum(axis=1)
ranked_teams = df[df['Total Votes'] > 0].values # returns each ranked team as a list with name then votes

teams = []
for team in ranked_teams:
    teams.append(
        go.Scatter(
            x=weeks,
            y=team[1:],
            name=team[0],
            line = dict(
                color = team_data.loc[team[0],'Primary Color'], #select team color from database
                width = 4)
            )
        )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Test 1'),
    html.Div(children='''
    This is a test!
    '''),

    dcc.Graph(
        id='test-graph',
        figure={
            'data': teams,
            'layout': go.Layout(
                xaxis={'title': 'Week'},
                yaxis={'title': 'Votes in the Coaches Poll'}
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)