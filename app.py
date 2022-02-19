from dash import Dash, dcc, html, Input, Output
import pandas as pd
import altair as alt
# from altair_data_server import data_server

# Handle large data sets by not embedding them in the notebook
alt.data_transformers.disable_max_rows()
# alt.data_transformers.enable('data_server')

# Read in data 
df = pd.read_csv("./spotify.csv")
# df = df.iloc[:4900, :]

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server


col_list = ['loudness', 'acousticness', 'speechiness', 'instrumentalness', 'tempo']

app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='danceability',  # REQUIRED to show the plot on the first page load
        style={'border-width': '0', 'width': '70%'},
        options=[{'label': col, 'value': col} for col in col_list])])
 

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'))
    
def plot_altair(xcol):
    chart = alt.Chart(df).mark_rect().encode(
        alt.X(xcol, bin=alt.Bin(maxbins=60)),
        alt.Y('energy', bin=alt.Bin(maxbins=60)),
        alt.Color('count()'),
        tooltip='danceability').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)