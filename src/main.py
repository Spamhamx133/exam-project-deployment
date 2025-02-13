import dash
import pandas as pd
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import mysql.connector
import os

# Database Credentials.
config = {
    'user': 'root',
    'password': 'BertramHaskins369',
    'host': '34.88.104.191',
    'database': 'pima_indians_diabetes'
}

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM diabetes")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    cursor.close()
    connection.close()
except mysql.connector.Error as error:
    print(f"Error: {error}")
    df = pd.DataFrame()  # Fallback to an empty DataFrame

# Calculate the average number of pregnancies
average_pregnancies = round(df['Pregnancies'].mean(), 2)

# Calculate the Glucose level
average_glucose = round(df['Glucose'].mean(), 2)

# Calculate the average blood pressure level
average_bloodpressure = round(df['BloodPressure'].mean(), 2)

# Calculate the average Insulin level
average_insulin = round(df['Insulin'].mean(), 2)

# Calculate the average BMI level
average_bmi = round(df['BMI'].mean(), 2)

# Calculate the average Age
average_age = round(df['Age'].mean(), 2)

outcome_counts = df['Outcome'].value_counts().reset_index()
outcome_counts.columns = ['Outcome', 'Count']
outcome_counts['Outcome'] = outcome_counts['Outcome'].astype(str)

df_new = df.drop('PatientID', axis=1)

# Count zeros per column
zeros_per_column = (df_new == 0).sum()

# Convert the Series to a DataFrame for Plotly Express
zeros_df = zeros_per_column.reset_index()
zeros_df.columns = ['Features', 'Number of Zeros']

num_rows = len(df.axes[0])

age_counts = df_new['Age'].value_counts().sort_index()

df['Outcome'] = df['Outcome'].astype('category')

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server in src/main.py

# Initial figures and dropdown options (handle empty DataFrame)
initial_x = df_new.columns[0] if not df_new.empty and len(df_new.columns) > 0 else None
initial_y = df_new.columns[1] if not df_new.empty and len(df_new.columns) > 1 else None

fig1 = px.pie(outcome_counts, names='Outcome', values='Count', title='Binary Feature Outcome',
              color="Outcome", color_discrete_sequence=['#ea8c55', '#ea526f'])
fig2 = px.scatter(df_new, x=initial_x, y=initial_y, title='Scatter-chart',
                  color_discrete_sequence=['#ea8c55', '#ea526f'])
fig3 = px.box(df_new, x=initial_x, title='Number of pregnancies',
              color_discrete_sequence=['#ea8c55', '#ea526f'])
fig4 = px.bar(zeros_df, x='Features', y='Number of Zeros', title='Number of Zeros per Feature',
              color_discrete_sequence=['#ea8c55', '#ea526f'])
fig5 = px.violin(df, x="Outcome", y="Age", color="Outcome", box=True, points="all",
              title="Age Distribution by Diabetes Outcome",
              color_discrete_sequence=['#ea8c55', '#ea526f'])

dropdown_options = [{'label': col, 'value': col} for col in df_new.columns] if not df_new.empty else []

app.layout = html.Div(children=[
html.Div(className="container-fluid", children=[
    html.H1(children="Diagnosis of Diabetes Dashboard", className="p-5 rounded-lg shadow",
            style={"background-color": '#d4652e', "margin-bottom": "20px", "color": "white"}),

        html.Div(className="row card-container",  children=[
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("👶 Average number of Pregnancies",  className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_pregnancies, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("🧪 Average Glucose level", className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_glucose, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("❤ Average Blood Pressure level", className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_bloodpressure, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("🧪 Average Insulin level", className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_insulin, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("💪 Average BMI", className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_bmi, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
            html.Div(className="col-md-2", children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        html.H5("⌛ Average Age", className="card-title", style={'filter': 'grayscale(100%)'}),
                        html.P(average_age, className="card-text", style={'text-indent': '33px', 'font-size': '18px', 'font-weight': 'bold'}),
                    ])
                ], style={"height": "100%"})
            ]),
        ], style={"padding-bottom": "10px"}),

    html.Div(className="row card-container", children=[
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dcc.Graph(figure=fig1),
                    html.P(f"Number of Data Points: {num_rows}", className="card-text", style={'text-align': 'center'}),
                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dcc.Graph(figure=fig4),
                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dcc.Graph(figure=fig5),
                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[
                    dcc.Graph(id='boxplot', figure=fig3),
                    dcc.Dropdown(
                        id='x-axis-dropdown1',
                        options=dropdown_options,
                        value=initial_x,
                        clearable=False
                    ),
                ])
            ], style={"height": "100%"})
        ]),
    ], style={"padding-bottom": "10px"}),
html.Div(className="row card-container", children=[
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                    dbc.CardBody(children=[
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
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[

                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                dbc.CardBody(children=[

                ])
            ], style={"height": "100%"})
        ]),
        html.Div(className="col-md-3", children=[
            dbc.Card(children=[
                    dbc.CardBody(children=[

                    ])
                ], style={"height": "100%"})
        ]),
    ], style={"padding-bottom": "10px"}),
]),
])

@app.callback(
    Output('boxplot', 'figure'),
    Input('x-axis-dropdown1', 'value')
)
def update_boxplot(x_value):
    if x_value and not df.empty:
        fig = px.box(df, x=x_value, color_discrete_sequence=['#ea8c55', '#ea526f'])
        fig.update_layout(title=f"{x_value}")
        return fig
    return {}

# Callback to update the scatter plot
@app.callback(
    Output('scatter-chart', 'figure'),
    Input('x-axis-dropdown2', 'value'),
    Input('y-axis-dropdown2', 'value')
)
def update_scatter_chart(x_value, y_value):
    if x_value and y_value and not df.empty:
        fig = px.scatter(df, x=x_value, y=y_value, color_discrete_sequence=['#ea8c55', '#ea526f'])
        fig.update_layout(title=f"{x_value} vs {y_value}")
        return fig
    return {}  

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)