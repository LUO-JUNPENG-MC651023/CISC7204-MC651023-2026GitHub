#!/usr/bin/env python
# coding: utf-8
"""
CISC7204 / DV0101EN - Final Project Part 02
Creating a Dashboard with Plotly and Dash
=========================================

Automobile Sales Statistics Dashboard

Reports produced by the dashboard
---------------------------------
1. Yearly Automobile Sales Statistics  (needs a year selection)
   - yearly average automobile sales, line chart (whole period)
   - total monthly automobile sales, line chart (selected year)
   - average vehicles sold by vehicle type, bar chart (selected year)
   - total advertisement expenditure by vehicle type, pie chart (selected year)

2. Recession Period Statistics         (year selection disabled)
   - average automobile sales fluctuation over recession period, line chart
   - average number of vehicles sold by vehicle type, bar chart
   - total expenditure share by vehicle type, pie chart
   - effect of unemployment rate on vehicle type and sales, bar chart

Run with:  python DV0101EN_Final_Assign_Part_2.py
Then open: http://127.0.0.1:8050
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# Load the Automobile Sales data with pandas.
# The course dataset is read from the cloud; if there is no internet
# connection the local copy (automobile_sales.csv, in the same folder) is used.
# ---------------------------------------------------------------------------
DATA_URL = ('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
            'd51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

try:
    data = pd.read_csv(DATA_URL)
except Exception:                      # offline fallback
    data = pd.read_csv('automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard (shown in the browser tab)
app.title = "Automobile Sales Statistics Dashboard"

# ---------------------------------------------------------------------------
# Dropdown menu options
# ---------------------------------------------------------------------------
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years covered by the dataset (1980 - 2023)
year_list = [i for i in range(1980, 2024, 1)]

# Calendar order of the months, used to keep the monthly line chart in order
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Shared style of the two dropdowns
dropdown_style = {
    'width': '80%',
    'padding': '3px',
    'fontSize': '20px',
    'textAlignLast': 'center'
}

# ---------------------------------------------------------------------------
# Layout of the app
# ---------------------------------------------------------------------------
app.layout = html.Div([

    # TASK 2.1: Title of the dashboard, centered, colour #503D36, font size 24
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}
    ),

    # TASK 2.2: First dropdown - report type
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style=dropdown_style
        )
    ]),

    # TASK 2.2: Second dropdown - year (enabled only for Yearly Statistics)
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder='Select-year',
            style=dropdown_style
        )
    ]),

    # TASK 2.3: Division used to display the output (the four charts)
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex', 'flexDirection': 'column'}
        ),
    ])
])


# ---------------------------------------------------------------------------
# TASK 2.4: Callbacks
# ---------------------------------------------------------------------------

# Enable / disable the year dropdown depending on the selected report type.
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    """Year can only be chosen for the 'Yearly Statistics' report."""
    if selected_statistics == 'Yearly Statistics':
        return False            # enable the year dropdown
    else:
        return True             # disable the year dropdown


# Build the four charts of the selected report.
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, input_year):
    """Return four charts (2 rows x 2 columns) for the selected report."""

    # ------------------------------------------------------------------
    # TASK 2.5: Recession Period Statistics
    # ------------------------------------------------------------------
    if selected_statistics == 'Recession Period Statistics':

        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: average automobile sales fluctuation over the recession
        # period, year wise (line chart)
        yearly_rec = (recession_data.groupby('Year')['Automobile_Sales']
                      .mean().reset_index())
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation over Recession Period"))

        # Plot 2: average number of vehicles sold by vehicle type (bar chart)
        average_sales = (recession_data.groupby('Vehicle_Type')['Automobile_Sales']
                         .mean().reset_index())
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type"))

        # Plot 3: total expenditure share by vehicle type during recessions
        # (pie chart)
        exp_rec = (recession_data.groupby('Vehicle_Type')['Advertising_Expenditure']
                   .sum().reset_index())
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Expenditure Share by Vehicle Type During Recessions'))

        # Plot 4: effect of the unemployment rate on vehicle type and sales
        # (bar chart)
        unemp_data = (recession_data
                      .groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales']
                      .mean().reset_index())
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate',
                        'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart1, style={'width': '50%'}),
                               html.Div(children=R_chart2, style={'width': '50%'})],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart3, style={'width': '50%'}),
                               html.Div(children=R_chart4, style={'width': '50%'})],
                     style={'display': 'flex'})
        ]

    # ------------------------------------------------------------------
    # TASK 2.6: Yearly Automobile Sales Statistics
    # ------------------------------------------------------------------
    elif selected_statistics == 'Yearly Statistics' and str(input_year).isdigit():

        # Keep only the rows of the selected year
        yearly_data = data[data['Year'] == int(input_year)]

        # Plot 1: yearly automobile sales over the whole period (line chart)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales over the Whole Period (1980 - 2023)'))

        # Plot 2: total monthly automobile sales for the selected year
        # (line chart)
        mas = (yearly_data.groupby('Month')['Automobile_Sales']
               .sum().reset_index())
        # groupby sorts the month names alphabetically, restore calendar order
        mas['Month'] = pd.Categorical(mas['Month'], categories=month_order, ordered=True)
        mas = mas.sort_values('Month').reset_index(drop=True)
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales in {}'.format(input_year)))

        # Plot 3: average number of vehicles sold by vehicle type in the
        # selected year (bar chart)
        avr_vdata = (yearly_data.groupby('Vehicle_Type')['Automobile_Sales']
                     .mean().reset_index())
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Plot 4: total advertisement expenditure for each vehicle type in the
        # selected year (pie chart)
        exp_data = (yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure']
                    .sum().reset_index())
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle Type in the year {}'.format(input_year)))

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart1, style={'width': '50%'}),
                               html.Div(children=Y_chart2, style={'width': '50%'})],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart3, style={'width': '50%'}),
                               html.Div(children=Y_chart4, style={'width': '50%'})],
                     style={'display': 'flex'})
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
