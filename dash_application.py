import dash
from dash import dcc 
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import db_access

app = dash.Dash(__name__) # Name der Applikation
df_raw = db_access.get_top_songs() #Daten aus der Datenbank

app.layout = html.Div(children=[
    html.H1(children='Analyse Spotify Charts'),
    html.Label("Select Country:"),
    dcc.Dropdown(id='my_dropdown_country', options=['Global', 'USA', 'UK', 'Italy', 'Germany', 'France', 
                                              'Spain', 'Netherlands', 'Iceland', 'Switzerland'], 
                                              value='Global'),
    html.Label("Select Y-Axis Values:"),
    dcc.Dropdown(id='my_dropdown_y', options=['Danceability', 'Energy', 'Speechiness', 
                                              'Acousticness', 'Instrumentalness', 'Liveness', 
                                              'Valence', 'Tempo', 'Rank', 'Popularity'], value='Danceability'),
    dcc.Graph(id='my_graph'),
    dcc.Graph(id='my_barchart')])

@app.callback(
    Output(component_id='my_graph', component_property='figure'),
    Output(component_id='my_barchart', component_property='figure'),
    [Input(component_id='my_dropdown_country', component_property='value'),
     Input(component_id='my_dropdown_y', component_property='value')]
)

def update_graphs(my_dropdown_country_value, my_dropdown_y_value):
    df_scatter = df_raw.query('Country == ' + "'" + my_dropdown_country_value + "'")
    df_bar = df_scatter.assign(Genres=df_scatter['Genres'].str.split(', ')).explode('Genres')

    df_bar_grouped_by = df_bar.groupby(['Genres']).agg({my_dropdown_y_value : 'mean'})
    df_bar_grouped_by = df_bar_grouped_by.sort_values(by=my_dropdown_y_value, ascending=False)
    df_bar_grouped_by_head = df_bar_grouped_by.head(8)
    # create a plotly figure based on the selected value
    try:
        fig = px.scatter(x=df_scatter['Rank'], y=df_scatter[my_dropdown_y_value], trendline='ols')
    except Exception as e:
        print(e)
        try:
            fig = px.scatter(x=df_scatter['Rank'], y=df_scatter[my_dropdown_y_value])
        except Exception as e:
            print(e)
    fig.update_xaxes(title='Rank')
    fig.update_yaxes(title=my_dropdown_y_value)

    fig_bar = px.bar(x=df_bar_grouped_by_head.index, y=df_bar_grouped_by_head[my_dropdown_y_value])
    fig_bar.update_xaxes(title='Genres')
    fig_bar.update_yaxes(title=my_dropdown_y_value)

    return fig, fig_bar


if __name__ == '__main__':
    app.run_server(debug=True)