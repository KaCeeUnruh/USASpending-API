# Import necessary libraries
import dash
import dash_table
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd

# Define the function to fetch data
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
server = app.server  # This is needed for Heroku deployment

# Define the app layout
app.layout = html.Div([
    html.H1("USA Government Spending",
        style={"textAlign": "center", "fontSize": 50, "fontFamily": "Times New Roman", "color": "rgb(51, 61, 90)"}),
    dbc.Button("Fetch Data",
        id="fetch-button",
        className="mb-3",
        style={"textAlign": "center", "fontSize": 20, "fontFamily": "Times New Roman", "color": "rgb(51, 61, 90)"}),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': i, 'id': i} for i in []], # Initially empty
        page_size=10,  # Number of rows per page
        style_cell={'textAlign': 'left', 'fontFamily': 'Times New Roman'},
        style_table={'fontSize': 12,},
        style_data={
            'color': 'rgb(51, 61, 90)',
            'backgroundColor': 'white'
         },
        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(240, 240, 240)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'color': 'rgb(51, 61, 90)',
            'fontWeight': 'bold',
            'fontFamily': 'Times New Roman'
            'fontSize': 15,
            }
    ),
])

# Define callback to update table
@app.callback(
    Output("data-table", "data"),
    Output("data-table", "columns"),
    [Input("fetch-button", "n_clicks")]
)
def update_table(n_clicks):
    if n_clicks:
        df = fetch_data()
        columns = [{"name": i, "id": i} for i in df.columns]
        return df.to_dict('records'), columns
    return [], []

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
