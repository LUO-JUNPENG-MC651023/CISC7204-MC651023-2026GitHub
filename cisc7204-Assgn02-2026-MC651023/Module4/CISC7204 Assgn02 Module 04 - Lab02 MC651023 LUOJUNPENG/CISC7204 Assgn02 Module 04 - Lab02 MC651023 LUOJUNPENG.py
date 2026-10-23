import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# 1. Data Preparation
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv"
df = pd.read_csv(url)
data = df.sample(n=500, random_state=42)

# 2. Create figure
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# 3. Initialize App
app = Dash(__name__)

# 4. App Layout (结合了 Task 3, 4, 5)
app.layout = html.Div(children=[
    html.H1('Airline On-Time Performance Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    html.P('Proportion of distance group (250 mile distance interval group) by flights.', 
           style={'textAlign': 'center', 'color': '#F57241'}),
    
    html.P('Practice Task: This pie chart shows the percentage of flights by distance group.', 
           style={'textAlign': 'center', 'color': '#333333'}),
    
    dcc.Graph(figure=fig)
])

# 5. Run App
if __name__ == '__main__':
    app.run(debug=True)