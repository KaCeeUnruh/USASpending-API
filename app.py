import requests

def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    data = response.json()
    return data["results"]

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Initialize the Dash app with Bootstrap's COSMO theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

# Layout for the front page
front_page = html.Div([
    dbc.Jumbotron([
        html.H1("USA Government Spending", className="display-3"),
        html.P(
            "Explore data on the top tier agencies.",
            className="lead",
        ),
        dbc.Button("Explore Data", id="explore-button", color="primary"),
    ]),
], style={"marginTop": "15%"})

# Layout for the data table
data_page = html.Div([
    dbc.Button("Fetch Data", id="fetch-button", color="primary", className="mb-3"),
    dbc.Table(id="data-table", bordered=True, striped=True, hover=True, responsive=True),
])

app.layout = html.Div(id='page-content', children=front_page)

@app.callback(
    Output('page-content', 'children'),
    [Input('explore-button', 'n_clicks')]
)
def display_page(n):
    if n:
        return data_page
    return front_page

@app.callback(
    Output("data-table", "children"),
    [Input("fetch-button", "n_clicks")]
)
def update_table(n_clicks):
    if n_clicks:
        data = fetch_data()
        table_header = [
            html.Thead(html.Tr([html.Th(column) for column in data[0].keys()]))
        ]
        table_body = [
            html.Tbody([
                html.Tr([html.Td(row[column]) for column in row.keys()]) for row in data
            ])
        ]
        return table_header + table_body
    return []

if __name__ == "__main__":
    app.run_server(debug=True)
