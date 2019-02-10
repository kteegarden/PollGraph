import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

file_path = os.path.join('C:/Users/Kyle Teegarden/Documents/Python Project/PollGraph', 'TestData.csv')
df = pd.read_csv(file_path)
df.set_index('Team', inplace=True)
print(df.iloc[0,:].values)
print(df.iloc[0,:].values)

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
            'data': [
                {'x': [1, 2, 3], 'y': df.iloc[0,:].values, 'type': 'line', 'name': 'Alabama'},
                {'x': [1, 2, 3], 'y': df.iloc[1,:].values, 'type': 'line', 'name': 'Virginia'}
            ],
            'layout': go.Layout(
                xaxis={'title': 'Week'},
                yaxis={'title': 'Votes in the Coaches Poll'}
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)