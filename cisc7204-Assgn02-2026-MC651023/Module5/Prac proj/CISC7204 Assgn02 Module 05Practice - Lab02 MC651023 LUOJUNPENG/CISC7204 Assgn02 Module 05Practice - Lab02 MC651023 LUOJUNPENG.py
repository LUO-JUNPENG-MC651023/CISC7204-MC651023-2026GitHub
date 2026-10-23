"""Module 05 - Practice Project - Part 02: Creating Dashboards.

Australia Wildfire Dashboard built with Dash.

The dashboard has two inputs (region radio items and year dropdown) and two
outputs (a pie chart and a bar chart) that are refreshed by a single callback.

Run with:
    python dash_wildfire.py
Then open http://127.0.0.1:8050 in a browser.
"""

import os
from pathlib import Path

import pandas as pd
import dash
from dash import Input, Output, dcc, html
import plotly.express as px

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/"
    "Data%20Files/Historical_Wildfires.csv"
)

# Use the local copy when it is available (works offline); otherwise download it.
DATA_FILE = Path(__file__).resolve().with_name("Historical_Wildfires.csv")


def load_wildfire_data() -> pd.DataFrame:
    """Read the wildfire dataset and derive the Month and Year columns."""
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.read_csv(DATA_URL)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month_name()  # used for the names of the months
    df["Year"] = df["Date"].dt.year
    return df


df = load_wildfire_data()

REGIONS = [
    {"label": "New South Wales", "value": "NSW"},
    {"label": "Northern Territory", "value": "NT"},
    {"label": "Queensland", "value": "QL"},
    {"label": "South Australia", "value": "SA"},
    {"label": "Tasmania", "value": "TA"},
    {"label": "Victoria", "value": "VI"},
    {"label": "Western Australia", "value": "WA"},
]
YEARS = sorted(int(year) for year in df["Year"].unique())

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)

# Do not display the "missing component" exception until the callback has run.
app.config.suppress_callback_exceptions = True

# Layout section of Dash
app.layout = html.Div(
    children=[
        # Task 2.1: title of the dashboard
        html.H1(
            "Australia Wildfire Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 26},
        ),
        # Task 2.2: inputs (region radio items and year dropdown)
        html.Div(
            [
                # First inner division: the input controls
                html.Div(
                    [
                        html.H2("Select Region:", style={"margin-right": "2em"}),
                        dcc.RadioItems(
                            options=REGIONS,
                            value="NSW",
                            id="region",
                            inline=True,
                        ),
                        html.Div(
                            [
                                html.H2(
                                    "Select Year", style={"margin-right": "2em"}
                                ),
                                dcc.Dropdown(YEARS, value=2005, id="year"),
                            ]
                        ),
                    ]
                ),
                # Task 2.3: second inner division with the two graph outputs
                html.Div(
                    [
                        html.Div([], id="plot1"),
                        html.Div([], id="plot2"),
                    ],
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)


# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------
# Task 2.4: input and output components of the callback
@app.callback(
    [
        Output("plot1", "children"),
        Output("plot2", "children"),
    ],
    [
        Input("region", "value"),
        Input("year", "value"),
    ],
)
# Task 2.5: callback function
def reg_year_display(input_region, input_year):
    # Data for the selected region and year
    region_data = df[df["Region"] == input_region]
    y_r_data = region_data[region_data["Year"] == input_year]

    # Plot one - Monthly Average Estimated Fire Area
    est_data = (
        y_r_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    )
    fig1 = px.pie(
        est_data,
        values="Estimated_fire_area",
        names="Month",
        title="{} : Monthly Average Estimated Fire Area in year {}".format(
            input_region, input_year
        ),
    )

    # Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby("Month")["Count"].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x="Month",
        y="Count",
        title="{} : Average Count of Pixels for Presumed Vegetation Fires in year {}".format(
            input_region, input_year
        ),
    )

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


if __name__ == "__main__":
    # Port 8050 by default; set the PORT environment variable to change it.
    app.run(debug=False, port=int(os.environ.get("PORT", "8050")))
