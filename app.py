# Import necessary libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd

# Define the function to fetch data and change column names
def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df = df.rename(columns={
        "agency_id": "Agency ID",
        "toptier_code": "Toptier Code",
        "agency_name": "Agency Name",
        "abbreviation": "Abbreviation",
        "congressional_justification_url": "Congressional Justification URL",
        "active_fy": "Active FY",
        "active_fq": "Active FQ",
        "outlay_amount": "Outlay Amount",
        "obligated_amount": "Obligated Amount",
        "budget_authority_amount": "Budget Authority Amount",
        "current_total_budget_authority_amount": "Current Total Budget Authority Amount",
        "percentage_of_total_budget_authority": "Percentage of Total Budget Authority",
        "agency_slug": "Agency Slug"
    })
    return df

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

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
        # Implementing basic pagination
        rows_per_page = 10
        start_idx = (page_number - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        df_page = df.iloc[start_idx:end_idx]
        table_header = [html.Thead(html.Tr([html.Th(column) for column in df.columns]))]
        table_body = [html.Tbody([html.Tr([html.Td(df.iloc[i][column]) for column in df.columns]) for i in range(len(df))])]
        return table_header + table_body
    return []

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
