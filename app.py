
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

# App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Datos
url = "https://raw.githubusercontent.com/fdealbam/feminicidios/main/application/feminicidios2015_2021.csv"
df = pd.read_csv(url).drop(columns=["Unnamed: 0"])
df['Total'] = df[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
                  'Agosto','Septiembre','Octubre','Noviembre','Diciembre']].sum(axis=1)
totales_anuales = df.groupby("Año")["Total"].sum().reset_index()

# Gráfica
fig = go.Figure()
fig.add_trace(go.Bar(x=totales_anuales["Año"], y=totales_anuales["Total"],
                     marker_color='indianred'))
fig.update_layout(title="Feminicidios por Año (2015–2021)",
                  xaxis_title="Año", yaxis_title="Total")

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Dashboard de Feminicidios en México (2015–2021)"), width=12)),
    dbc.Row(dbc.Col(dcc.Graph(figure=fig), width=12)),
    dbc.Row(dbc.Col(html.P("Fuente: SESNSP"), width=12)),
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)

