import dash
import pandas as pd
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import mysql.connector
import os  # For environment variables

# --- Configuration (Move to a config file or environment variables) ---
DB_HOST = os.environ.get("DB_HOST") or "localhost"  # Use environment variables
DB_USER = os.environ.get("DB_USER") or "root"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or "pass123"
DB_NAME = os.environ.get("DB_NAME") or "pima_diabetes"

# --- Database Connection ---
try:
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    df = pd.read_sql("SELECT Pregnancies, Glucose, BloodPressure, Insulin, BMI, Age, df, Outcome FROM patients", conn) # Simpler way to read SQL
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    df = pd.DataFrame()  # Empty DataFrame on error
finally:
    if conn and conn.is_connected():
        conn.close()

# --- Data Processing ---
if not df.empty:  # Check if DataFrame is populated
    outcome_counts = df['Outcome'].value_counts().reset_index()
    outcome_counts.columns = ['Outcome', 'Count']
    outcome_counts['Outcome'] = outcome_counts['Outcome'].astype(str)  # Convert to string

    # --- Initial Figures (using better defaults) ---
    initial_x = df.columns[0]
    initial_y = df.columns[1]

    fig1 = px.bar(outcome_counts, x='Outcome', y='Count', title='Binary Variable Outcome', color_discrete_sequence=px.colors.sequential.Viridis)
    fig2 = px.scatter(df, x=initial_x, y=initial_y, title='Scatter Chart', color_discrete_sequence=px.colors.sequential.Viridis)  # More descriptive title
    fig3 = px.histogram(df, x=initial_x, title='Histogram', color_discrete_sequence=px.colors.sequential.Viridis)

    dropdown_options = [{'label': col, 'value': col} for col in df.columns]

else:  # Handle the case where the DataFrame is empty
    fig1 = px.bar(title='No data available')  # Empty figures
    fig2 = px.scatter(title='No data available')
    fig3 = px.histogram(title='No data available')
    dropdown_options = []


# --- Dash App Layout ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Diagnosis of Diabetes Dashboard", className="p-5 rounded-lg shadow", style={"background-color": '#482878', "margin-bottom": "20px", "color": "white"}),

    # ... (Card layout - Consider using a loop to generate these) ...
    # Example using a loop (requires data about the cards)

    # --- Graphs and Dropdowns ---
    html.Div(className="row card-container", children=[
        html.Div(className="col-md-4", children=[
            dbc.Card(children=[
                dbc.CardBody([
                    html.H5("Histogram", className="card-title"),  # More descriptive title
                    dcc.Graph(id='histogram', figure=fig3),
                    dcc.Dropdown(id='x-axis-dropdown1', options=dropdown_options, value=initial_x, clearable=False),
                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-4", children=[  # Scatter plot card
            dbc.Card(children=[
                dbc.CardBody([
                    html.H5("Scatter Chart", className="card-title"),  # More descriptive title
                    dcc.Graph(id='scatter-chart', figure=fig2),
                    dcc.Dropdown(id='x-axis-dropdown2', options=dropdown_options, value=initial_x, clearable=False),
                    dcc.Dropdown(id='y-axis-dropdown2', options=dropdown_options, value=initial_y, clearable=False),
                ])
            ], style={"height": "100%"})
        ]),
        # ... (Other graph cards) ...
    ]),

    # ... (Other rows of cards) ...

], style={"height": "100%"})  # Set height for the main div

# --- Callbacks ---
@app.callback(
    Output('histogram', 'figure'),
    Input('x-axis-dropdown1', 'value')
)
def update_histogram(x_value):
    if x_value and not df.empty:
        fig = px.histogram(df, x=x_value, color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(title=f"Histogram - {x_value}")  # More consistent title
        return fig
    return dash.no_update  # Use dash.no_update for efficiency

@app.callback(
    Output('scatter-chart', 'figure'),
    Input('x-axis-dropdown2', 'value'),
    Input('y-axis-dropdown2', 'value')
)
def update_scatter_chart(x_value, y_value):
    if x_value and y_value and not df.empty:
        fig = px.scatter(df, x=x_value, y=y_value, color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(title=f"Scatter Chart - {x_value} vs {y_value}")  # More consistent title
        return fig
    return dash.no_update  # Use dash.no_update

# ... (Other callbacks)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)  # Use run_server