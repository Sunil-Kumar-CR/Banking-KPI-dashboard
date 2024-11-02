# Import required libraries
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Sample data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["NY", "NY", "NY", "LA", "LA", "LA"]
})

# Plotly express bar chart
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children="Dash App Example"),
    
    html.Div(children="""
        A simple bar chart example with Dash.
    """),
    
    dcc.Graph(
        id="example-graph",
        figure=fig
    )
])

# This will be used for testing here on wards
# some more changes 

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
