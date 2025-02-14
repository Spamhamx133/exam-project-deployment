import dash
import pandas as pd
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import mysql.connector

# Database connection details (move to a config file for production)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'pass123'
DB_NAME = 'pima_diabetes'

try:
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT Pregnancies, Glucose, BloodPressure, Insulin, BMI, Age, df, Outcome FROM patients;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Get column names from the cursor description
    column_names = [description[0] for description in cursor.description]

    df = pd.DataFrame(results, columns=column_names)

    df.head()

except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    df = pd.DataFrame()  # Create an empty DataFrame if connection fails
finally:
    if conn and conn.is_connected():  # Check if connection exists before calling is_connected()
        cursor.close()
        conn.close()

# Count the occurrences of 0 and 1
outcome_counts = df['Outcome'].value_counts().reset_index()
outcome_counts.columns = ['Outcome', 'Count']

# Convert 'Outcome' to string for better display in Plotly
outcome_counts['Outcome'] = outcome_counts['Outcome'].astype(str)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initial figures (using the first two columns as defaults)
initial_x = df.columns[0] if not df.empty and len(df.columns) > 0 else None
initial_y = df.columns[1] if not df.empty and len(df.columns) > 1 else None

fig1 = px.bar(outcome_counts, x='Outcome', y='Count', title='Binary Variable Outcome', color_discrete_sequence=px.colors.sequential.Viridis)
fig2 = px.scatter(df, x=initial_x, y=initial_y, title='Scatter-chart', color_discrete_sequence=px.colors.sequential.Viridis)
fig3 = px.histogram(df, x=initial_x, title='Histogram', color_discrete_sequence=px.colors.sequential.Viridis)


# Create dropdown options dynamically from DataFrame columns
dropdown_options = [{'label': col, 'value': col} for col in df.columns] if not df.empty else []


app.layout = html.Div(children=[
    html.H1(children="Diagnosis of Diabetes Dashboard", className="p-5 rounded-lg shadow",
            style={"background-color": '#482878', "margin-bottom": "20px", "color": "white"}),

    html.Div(className="container-fluid", children=[
        html.Div(className="row card-container", children=[
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("Pregnancies", className="card-title"),
                        html.P("Some quick example text.", className="card-text"),
                    ])
                ], style={"height": "100%"})

            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("Glucose", className="card-title"),
                        html.P("Some quick example text.", className="card-text"),
                    ])
                ], style={"height": "100%"})

            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("BloodPressure", className="card-title"),
                        html.P("Some quick example text.", className="card-text"),
                    ])
                ], style={"height": "100%"})

            ]),
        html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                dbc.CardBody(children=[
                    html.H5("Insulin", className="card-title"),
                    html.P("Some quick example text.", className="card-text"),
                ])
            ], style={"height": "100%"})

            ]),
        html.Div(className="col-md-2", children=[
                 dbc.Card(children=[
                 dbc.CardBody(children=[
                    html.H5("BMI", className="card-title"),
                    html.P("Some quick example text.", className="card-text"),
                ])
            ], style={"height": "100%"})

        ]),
        html.Div(className="col-md-2", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    html.H5("Age", className="card-title"),
                    html.P("Some quick example text.", className="card-text"),
                ])
            ], style={"height": "100%"})
        ]),
    ], style={"padding-bottom": "10px"}),
]),

        html.Div(className="row card-container", children=[
            html.Div(className="col-md-4", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("Card 7", className="card-title"),
                        dcc.Graph(id='histogram', figure=fig3),
                        dcc.Dropdown(
                            id='x-axis-dropdown1',
                            options=dropdown_options,
                            value=initial_x,
                            clearable=False
                        ),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-4", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("Card 8", className="card-title"),
                        dcc.Graph(id='scatter-chart', figure=fig2),
                        dcc.Dropdown(
                            id='x-axis-dropdown2',
                            options=dropdown_options,
                            value=initial_x,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id='y-axis-dropdown2',
                            options=dropdown_options,
                            value=initial_y,
                            clearable=False
                        ),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-4", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("Card 9", className="card-title"),
                        dcc.Graph(figure=fig3),
                    ])
                ], style={"height": "100%"})
            ]),
        ], style={"padding-bottom": "10px"}),

    html.Div(className="row card-container", children=[
        html.Div(className="col-md-6", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    html.H5("Card 10", className="card-title"),
                    dcc.Graph(figure=fig1),
                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-6", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    html.H5("Card 11", className="card-title"),
                    dcc.Graph(figure=fig1),
                ])
            ], style={"height": "100%"})
        ]),
    ]),
], style={"height": "100%"})


@app.callback(
    Output('histogram', 'figure'),
    Input('x-axis-dropdown1', 'value'),
    State('histogram', 'figure')
)
def update_histogram(x_value, current_fig):
    if x_value and not df.empty:
        fig = px.histogram(df, x=x_value, color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(title=f"histogram - {x_value}")
        return fig
    return current_fig if current_fig else {}  # Return current or empty if no current


@app.callback(
    Output('scatter-chart', 'figure'),
    Input('x-axis-dropdown2', 'value'),
    Input('y-axis-dropdown2', 'value'),
    State('scatter-chart', 'figure')
)
def update_scatter_chart(x_value, y_value, current_fig):
    if x_value and y_value and not df.empty:
        fig = px.scatter(df, x=x_value, y=y_value, color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(title=f"{x_value} vs {y_value}")
        return fig
    return current_fig if current_fig else {}  # Return current or empty if no current


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)