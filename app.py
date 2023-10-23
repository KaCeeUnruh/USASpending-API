import requests
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table


def fetch_data():
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data["results"])

# Initialize the Dash app with Bootstrap's COSMO theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server  # This is for deployment

# Layout for the data page
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
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
    html.Br(),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='datatable',
                    columns=[
                            {"name": "Agency ID", "id": "agency_id"},
                            {"name": "Toptier Code", "id": "toptier_code"},
                            {"name": "Agency Name", "id": "agency_name"},
                            {"name": "Abbreviation", "id": "abbreviation"},
                            {"name": "Congressional Justification URL", "id": "congressional_justification_url"},
                            {"name": "Active FY", "id": "active_fy"},
                            {"name": "Active FQ", "id": "active_fq"},
                            {"name": "Outlay Amount", "id": "outlay_amount"},
                            {"name": "Obligated Amount", "id": "obligated_amount"},
                            {"name": "Budget Authority Amount", "id": "budget_authority_amount"},
                            {"name": "Current Total Budget Authority Amount",
                             "id": "current_total_budget_authority_amount"},
                            {"name": "Percentage of Total Budget Authority",
                             "id": "percentage_of_total_budget_authority"},
                            {"name": "Agency Slug", "id": "agency_slug"}
                        ],
                    style={"fontFamily": "Balto"},
                    data=[],
                    style_table={
                    'backgroundColor': 'white',
                    },
                    style_cell={
                    'backgroundColor': 'white',
                    'color': 'black',
                },
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_current=0,
                page_size=10,
            ),
],
fluid=True)

])


@app.callback(
    Output("data-table", "children"),
    [Input("fetch-button", "n_clicks"), Input('row-selector', 'value')]
)

def update_table(n_clicks):
    if not n_clicks:
        return []

    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['results']
    else:
        return []


if __name__ == "__main__":
    app.run_server(debug=True)
