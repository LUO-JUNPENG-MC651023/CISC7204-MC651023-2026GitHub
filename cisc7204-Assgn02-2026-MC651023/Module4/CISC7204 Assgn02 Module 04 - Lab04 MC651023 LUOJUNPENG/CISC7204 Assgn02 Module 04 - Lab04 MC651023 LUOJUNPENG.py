"""Module 04 Lab 04: Flight Delay Time Statistics Dashboard.

Run with:
    python flight_delay.py

Then open http://127.0.0.1:8050 in a browser.
"""

import os
from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# ---------------------------------------------------------------------------
# Read the airline data into a pandas DataFrame
# ---------------------------------------------------------------------------
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "airline_data.csv"
)
# Keep a local copy next to this script so the dashboard also works offline.
# If the file is not present, the public course URL is used instead.
LOCAL_DATA_FILE = Path(__file__).resolve().with_name("airline_data.csv")
DATA_SOURCE = LOCAL_DATA_FILE if LOCAL_DATA_FILE.exists() else DATA_URL

airline_data = pd.read_csv(
    DATA_SOURCE,
    encoding="ISO-8859-1",
    dtype={
        "Div1Airport": str,
        "Div1TailNum": str,
        "Div2Airport": str,
        "Div2TailNum": str,
    },
)

# ---------------------------------------------------------------------------
# Build the Dash application and its layout
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Flight Delay Time Statistics",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 30,
            },
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id="input-year",
                    value="2018",
                    type="number",
                    min=2010,
                    max=2020,
                    step=1,
                    style={"height": "35px", "font-size": 30},
                ),
            ],
            style={"font-size": 30},
        ),
        html.Br(),
        html.Br(),
        # Segment 1
        html.Div(
            [
                html.Div(dcc.Graph(id="carrier-plot")),
                html.Div(dcc.Graph(id="weather-plot")),
            ],
            style={"display": "flex"},
        ),
        # Segment 2
        html.Div(
            [
                html.Div(dcc.Graph(id="nas-plot")),
                html.Div(dcc.Graph(id="security-plot")),
            ],
            style={"display": "flex"},
        ),
        # Segment 3
        html.Div(dcc.Graph(id="late-plot"), style={"width": "65%"}),
    ]
)


# ---------------------------------------------------------------------------
# Supporting computation function
# ---------------------------------------------------------------------------
def compute_info(airline_data, entered_year):
    """Compute the five average delay DataFrames for the selected year.

    Arguments:
        airline_data: Input airline data.
        entered_year: Input year for which computation needs to be performed.

    Returns:
        Average DataFrames for carrier, weather, NAS, security, and late
        aircraft delays, grouped by month and reporting airline.
    """
    # Select data
    df = airline_data[airline_data["Year"] == int(entered_year)]

    # Compute delay averages
    avg_car = (
        df.groupby(["Month", "Reporting_Airline"])["CarrierDelay"]
        .mean()
        .reset_index()
    )
    avg_weather = (
        df.groupby(["Month", "Reporting_Airline"])["WeatherDelay"]
        .mean()
        .reset_index()
    )
    avg_NAS = (
        df.groupby(["Month", "Reporting_Airline"])["NASDelay"]
        .mean()
        .reset_index()
    )
    avg_sec = (
        df.groupby(["Month", "Reporting_Airline"])["SecurityDelay"]
        .mean()
        .reset_index()
    )
    avg_late = (
        df.groupby(["Month", "Reporting_Airline"])["LateAircraftDelay"]
        .mean()
        .reset_index()
    )

    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# ---------------------------------------------------------------------------
# Callback
# ---------------------------------------------------------------------------
@app.callback(
    [
        Output(component_id="carrier-plot", component_property="figure"),
        Output(component_id="weather-plot", component_property="figure"),
        Output(component_id="nas-plot", component_property="figure"),
        Output(component_id="security-plot", component_property="figure"),
        Output(component_id="late-plot", component_property="figure"),
    ],
    Input(component_id="input-year", component_property="value"),
)
def get_graph(entered_year):
    """Return the five figures for the year entered by the user."""
    # Keep the dashboard usable if the input is cleared or is outside the
    # 2010-2020 range covered by the lab.
    try:
        entered_year = int(entered_year)
    except (TypeError, ValueError):
        entered_year = 2018
    if not 2010 <= entered_year <= 2020:
        entered_year = 2018

    # Compute required information for creating graphs from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(
        airline_data, entered_year
    )

    # Line plot for carrier delay
    carrier_fig = px.line(
        avg_car,
        x="Month",
        y="CarrierDelay",
        color="Reporting_Airline",
        title="Average carrier delay time (minutes) by airline",
        labels={"CarrierDelay": "CarrierDelay", "Month": "Month"},
    )

    # Line plot for weather delay
    weather_fig = px.line(
        avg_weather,
        x="Month",
        y="WeatherDelay",
        color="Reporting_Airline",
        title="Average weather delay time (minutes) by airline",
        labels={"WeatherDelay": "WeatherDelay", "Month": "Month"},
    )

    # Line plot for NAS delay
    nas_fig = px.line(
        avg_NAS,
        x="Month",
        y="NASDelay",
        color="Reporting_Airline",
        title="Average NAS delay time (minutes) by airline",
        labels={"NASDelay": "NASDelay", "Month": "Month"},
    )

    # Line plot for security delay
    sec_fig = px.line(
        avg_sec,
        x="Month",
        y="SecurityDelay",
        color="Reporting_Airline",
        title="Average security delay time (minutes) by airline",
        labels={"SecurityDelay": "SecurityDelay", "Month": "Month"},
    )

    # Line plot for late aircraft delay
    late_fig = px.line(
        avg_late,
        x="Month",
        y="LateAircraftDelay",
        color="Reporting_Airline",
        title="Average late aircraft delay time (minutes) by airline",
        labels={"LateAircraftDelay": "LateAircraftDelay", "Month": "Month"},
    )

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=int(os.environ.get("PORT", "8050")))
