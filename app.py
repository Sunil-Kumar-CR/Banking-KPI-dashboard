from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('test.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    html.H1("Insurance Customer Dashboard", style={'text-align': 'center'}),

    # Row for Count Metrics
    dbc.Row([
        dbc.Col(html.Div([
            html.H5("Total Customers"),
            html.H3(df.shape[0])
        ]), width=2),
        dbc.Col(html.Div([
            html.H5("Driving License Holders"),
            html.H3(df['Driving_License'].sum())
        ]), width=2),
        dbc.Col(html.Div([
            html.H5("Previously Insured"),
            html.H3(df['Previously_Insured'].sum())
        ]), width=2),
    ], justify="center"),

    html.Br(),

    # Modal Button and Modal
    dbc.Button("Show Detailed Counts", id="open-modal", n_clicks=0, className="mb-3"),
    dbc.Modal(
        [
            dbc.ModalHeader("Detailed Counts"),
            dbc.ModalBody([
                html.Div(f"Gender Distribution: {df['Gender'].value_counts().to_dict()}"),
                html.Div(f"Vehicle Age Distribution: {df['Vehicle_Age'].value_counts().to_dict()}"),
                html.Div(f"Vehicle Damage Distribution: {df['Vehicle_Damage'].value_counts().to_dict()}"),
                html.Div(f"Region Code Distribution: {df['Region_Code'].nunique()} unique regions")
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ml-auto", n_clicks=0)
            ),
        ],
        id="modal",
        is_open=False,
    ),

    html.Br(),

    # Dropdown for drill-down options
    dcc.Dropdown(
        id="filter-region",
        options=[{"label": f"Region {int(x)}", "value": x} for x in df["Region_Code"].unique()],
        placeholder="Filter by Region Code",
        style={"width": "50%"}
    ),

    html.Br(),

    # Bar chart for Vehicle Age vs. Vehicle Damage with updated colors
    dcc.Graph(id="bar-chart", config={'displayModeBar': False}),

    # Line chart for Average Premium by Age
    dcc.Graph(id="line-chart", config={'displayModeBar': False}),

    # Additional visualizations
    dbc.Row([
        dbc.Col(dcc.Graph(id="premium-histogram"), width=6),
        dbc.Col(dcc.Graph(id="gender-pie"), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="premium-boxplot"), width=6),
        dbc.Col(dcc.Graph(id="vehicle-damage-pie"), width=6),
    ]),
])

# Modal open/close callbacks
@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# Bar chart callback with improved color and background color
@app.callback(
    Output("bar-chart", "figure"),
    [Input("filter-region", "value")]
)
def update_bar_chart(region_code):
    if region_code:
        df_filtered = df[df["Region_Code"] == region_code]
    else:
        df_filtered = df
    fig = px.bar(
        df_filtered, x="Vehicle_Age", color="Vehicle_Damage",
        color_discrete_map={'Yes': '#FF6347', 'No': '#4682B4'},
        title="Vehicle Age vs Vehicle Damage"
    )
    fig.update_layout(
        barmode="group",
        plot_bgcolor="white",  # Set background color for plot area
        paper_bgcolor="white",  # Set background color for overall chart area
        title_font=dict(size=16),
        font=dict(color="black"),
        xaxis=dict(title="Vehicle Age", showgrid=True, gridcolor="lightgray"),
        yaxis=dict(title="Count", showgrid=True, gridcolor="lightgray"),
    )
    return fig

# Line chart callback for Average Premium by Age
@app.callback(
    Output("line-chart", "figure"),
    [Input("filter-region", "value")]
)
def update_line_chart(region_code):
    if region_code:
        df_filtered = df[df["Region_Code"] == region_code]
    else:
        df_filtered = df
    avg_premium = df_filtered.groupby("Age")["Annual_Premium"].mean().reset_index()
    fig = px.line(avg_premium, x="Age", y="Annual_Premium", title="Average Annual Premium by Age")
    return fig

# Histogram for Annual Premium
@app.callback(
    Output("premium-histogram", "figure"),
    [Input("filter-region", "value")]
)
def update_premium_histogram(region_code):
    df_filtered = df[df["Region_Code"] == region_code] if region_code else df
    fig = px.histogram(df_filtered, x="Annual_Premium", title="Distribution of Annual Premiums")
    return fig

# Pie chart for Gender Distribution
@app.callback(
    Output("gender-pie", "figure"),
    [Input("filter-region", "value")]
)
def update_gender_pie(region_code):
    df_filtered = df[df["Region_Code"] == region_code] if region_code else df
    fig = px.pie(df_filtered, names="Gender", title="Gender Distribution")
    return fig

# Box plot for Annual Premium by Vehicle Age
@app.callback(
    Output("premium-boxplot", "figure"),
    [Input("filter-region", "value")]
)
def update_premium_boxplot(region_code):
    df_filtered = df[df["Region_Code"] == region_code] if region_code else df
    fig = px.box(df_filtered, x="Vehicle_Age", y="Annual_Premium", title="Annual Premium by Vehicle Age")
    return fig

# Pie chart for Vehicle Damage Distribution
@app.callback(
    Output("vehicle-damage-pie", "figure"),
    [Input("filter-region", "value")]
)
def update_vehicle_damage_pie(region_code):
    df_filtered = df[df["Region_Code"] == region_code] if region_code else df
    fig = px.pie(df_filtered, names="Vehicle_Damage", title="Vehicle Damage Distribution")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
