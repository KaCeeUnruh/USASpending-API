# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd

# Define the function to fetch data
def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data['results'])

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server  # This is needed for Heroku deployment

# Define the app layout
app.layout = html.Div([
    html.H1("USA Government Spending", style={"textAlign": "center"}),
    dbc.Button("Fetch Data", id="fetch-button", className="mb-3"),
    dbc.Table(id="data-table", bordered=True, striped=True, hover=True, responsive=True),
])

# Define callback to update table
@app.callback(
    Output("data-table", "children"),
    Input("fetch-button", "n_clicks")
)
def update_table(n_clicks):
    if n_clicks:
        df = fetch_data()
        table_header = [html.Thead(html.Tr([html.Th(column) for column in df.columns]))]
        table_body = [html.Tbody([html.Tr([html.Td(df.iloc[i][column]) for column in df.columns]) for i in range(len(df))])]
        return table_header + table_body
    return []

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
