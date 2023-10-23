import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import requests

# Set up the app with external stylesheets from dash-bootstrap-components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server  # This is for deployment

# Define the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("USA Government Spending Data", className="text-center mt-4 mb-4"),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Fetch Data", id="fetch-button", color="secondary", className="mb-3"),
            dbc.Table(id="data-table", bordered=True, striped=True, hover=True, responsive=True),
        ])
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
                    {"name": "Current Total Budget Authority Amount", "id": "current_total_budget_authority_amount"},
                    {"name": "Percentage of Total Budget Authority", "id": "percentage_of_total_budget_authority"},
                    {"name": "Agency Slug", "id": "agency_slug"}
                ],
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
        ])
    ]),
], fluid=True)

# Define callback to update table data
@app.callback(
    Output('datatable', 'data'),
    Input('fetch-button', 'n_clicks')
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

if __name__ == '__main__':
    app.run_server(debug=False)
