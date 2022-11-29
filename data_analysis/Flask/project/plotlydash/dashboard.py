"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd

from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css",
        ],
    )

    # Load DataFrame
    df = create_dataframe()

    # Custom HTML layout
    #dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            
            create_data_table(df),
        ],
        id="dash-container",
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
        style_as_list_view=True,
        style_header={ 'border': '1px solid black' },
    )
    
    return table
