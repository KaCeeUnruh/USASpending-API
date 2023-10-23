import requests
import pandas as pd

def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data["results"])


import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Initialize the Dash app with Bootstrap's COSMO theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server  # This is for deployment

# Layout for the data page
app.layout = dbc.Container([
    html.H1("USA Government Spending", style={"textAlign": "center", "marginBottom": "40px"}),
    dbc.Row([
        dbc.Col(dbc.Button("Fetch Data", id="fetch-button", color="primary", className="mb-3")),
        dbc.Col(dcc.Dropdown(
            id='row-selector',
            options=[
                {'label': '10 Rows', 'value': 10},
                {'label': '20 Rows', 'value': 20},
                {'label': 'All Rows', 'value': 'all'}
            ],
            value=10,
            clearable=False
        ))
    ]),
    dbc.Table(id="data-table", style={"fontFamily": "Balto"}),
])


@app.callback(
    Output("data-table", "children"),
    [Input("fetch-button", "n_clicks"), Input('row-selector', 'value')]
)
def update_table(n_clicks, rows):
    if n_clicks:
        df = fetch_data()

        # If specific rows are selected, slice the dataframe
        if rows != 'all':
            df = df.head(rows)

        table_header = [
            html.Thead(html.Tr([html.Th(column) for column in df.columns]))
        ]
        table_body = [
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][column]) for column in df.columns]) for i in range(len(df))
            ])
        ]
        return table_header + table_body
    return []


if __name__ == "__main__":
    app.run_server(debug=True)
