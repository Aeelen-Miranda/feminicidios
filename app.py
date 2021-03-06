import dash
import matplotlib.pyplot as plt 
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import dash_table
import sidetable as stb
import datetime
from datetime import datetime, timedelta
from datetime import date
import geopandas as gpd
import flask
import os

yesterday = datetime.now() - timedelta(1)
yea = datetime.strftime(yesterday, '%Y%m%d')

today = date.today()
d2 = today.strftime("Fecha de actualización : %d-%m-%Y")



###############################
# DATABASES
############################### Abre archivos


#os.chdir(r"C:\Users\PRIME\AnacondaProjects\Project_curso\\")

delitos = pd.read_csv("https://raw.githubusercontent.com/fdealbam/feminicidios/main/application/feminicidios2015_2020.csv?raw=true")
delitos.drop('Unnamed: 0',1, inplace=True)

delitos.groupby(['Año','Entidad','Tipo de delito'])['Enero', 
                 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
       'Julio', 'Agosto', 'Septiembre', 'Octubre',
       'Noviembre', 'Diciembre'].sum().to_csv("00.csv",  header=True)

fem= pd.read_csv("00.csv")

############################################### separación de años

year15= fem[fem.Año == 2015]
year16= fem[fem.Año == 2016]
year17= fem[fem.Año == 2017]
year18= fem[fem.Año == 2018]
year19= fem[fem.Año == 2019]
year20= fem[fem.Año == 2020]

############################################### Agregar suffix de años

y15 = year15.add_suffix('15')
y15.rename(columns ={'Año15': 'Año', 'Tipo de delito15': 'Tipo de delito', 'Unnamed: 015' : 'Unnamed: 0',
                            'Entidad15': 'Entidad'}, inplace = True)

y16 = year16.add_suffix('16')
y16.rename(columns ={'Año16': 'Año', 'Tipo de delito16': 'Tipo de delito', 'Unnamed: 016' : 'Unnamed: 0',
                            'Entidad16': 'Entidad'}, inplace = True)

y17 = year17.add_suffix('17')
y17.rename(columns ={'Año17': 'Año', 'Tipo de delito17': 'Tipo de delito', 'Unnamed: 017' : 'Unnamed: 0',
                            'Entidad17': 'Entidad'}, inplace = True)

y18= year18.add_suffix('18')
y18.rename(columns ={'Año18': 'Año', 'Tipo de delito18': 'Tipo de delito','Unnamed: 018' : 'Unnamed: 0',
                            'Entidad18': 'Entidad'}, inplace = True)

y19= year19.add_suffix('19')
y19.rename(columns ={'Año19': 'Año', 'Tipo de delito19': 'Tipo de delito', 'Unnamed: 019' : 'Unnamed: 0',
                            'Entidad19': 'Entidad'}, inplace = True)

y20= year20.add_suffix('20')
y20.rename(columns ={'Año20': 'Año', 'Tipo de delito20': 'Tipo de delito','Unnamed: 020' : 'Unnamed: 0',
                            'Entidad20': 'Entidad'}, inplace = True)



############################################### Concat todos los años

fa = y15.merge(y16, on="Entidad",  how="inner")
fb = fa.merge(y17, on="Entidad",  how="inner")
fc = fb.merge(y18, on="Entidad",  how="inner")
fd = fc.merge(y19, on="Entidad",  how="inner")
fe = fd.merge(y20, on="Entidad",  how="inner")
                      
femi15_20 = fe[[
 'Entidad','Enero15','Febrero15','Marzo15','Abril15','Mayo15','Junio15',
 'Julio15','Agosto15','Septiembre15','Octubre15','Noviembre15','Diciembre15',
 
 'Enero16','Febrero16','Marzo16','Abril16','Mayo16','Junio16','Julio16',
 'Agosto16','Septiembre16','Octubre16','Noviembre16','Diciembre16',

 'Enero17','Febrero17','Marzo17','Abril17','Mayo17','Junio17','Julio17',
 'Agosto17','Septiembre17','Octubre17','Noviembre17','Diciembre17',
    
 'Enero18','Febrero18','Marzo18','Abril18','Mayo18','Junio18','Julio18',
 'Agosto18','Septiembre18','Octubre18','Noviembre18','Diciembre18',
 
 'Enero19','Febrero19','Marzo19','Abril19','Mayo19','Junio19','Julio19',
 'Agosto19','Septiembre19','Octubre19','Noviembre19','Diciembre19',

 'Enero20','Febrero20','Marzo20','Abril20','Mayo20','Junio20','Julio20',
 'Agosto20','Septiembre20','Octubre20','Noviembre20','Diciembre20']]


##CRear columna de TOTAL ANUAL 
femi15_20['Total2015']= femi15_20[[ 'Enero15', 'Febrero15', 'Marzo15', 'Abril15', 'Mayo15',
                               'Junio15', 'Julio15', 'Agosto15', 'Septiembre15', 'Octubre15',
                               'Noviembre15', 'Diciembre15',]].sum(axis=1)
femi15_20['Total2016']= femi15_20[[ 'Enero16', 'Febrero16', 'Marzo16', 'Abril16', 'Mayo16',
                               'Junio16', 'Julio16', 'Agosto16', 'Septiembre16', 'Octubre16',
                               'Noviembre16', 'Diciembre16',]].sum(axis=1)
femi15_20['Total2017']= femi15_20[[ 'Enero17', 'Febrero17', 'Marzo17', 'Abril17', 'Mayo17',
                               'Junio17', 'Julio17', 'Agosto17', 'Septiembre17', 'Octubre17',
                               'Noviembre17', 'Diciembre17',]].sum(axis=1)
femi15_20['Total2018']= femi15_20[[ 'Enero18', 'Febrero18', 'Marzo18', 'Abril18', 'Mayo18',
                               'Junio18', 'Julio18', 'Agosto18', 'Septiembre18', 'Octubre18',
                               'Noviembre18', 'Diciembre18',]].sum(axis=1)
femi15_20['Total2019']= femi15_20[[ 'Enero19', 'Febrero19', 'Marzo19', 'Abril19', 'Mayo19',
                               'Junio19', 'Julio19', 'Agosto19', 'Septiembre19', 'Octubre19',
                               'Noviembre19', 'Diciembre19',]].sum(axis=1)
femi15_20['Total2020']= femi15_20[[ 'Enero20', 'Febrero20', 'Marzo20', 'Abril20', 'Mayo20',
                               'Junio20', 'Julio20', 'Agosto20', 'Septiembre20', 'Octubre20',
                               'Noviembre20', 'Diciembre20',]].sum(axis=1)


#identificadores
conf_2015= femi15_20.Total2015.sum()
conf_2016= femi15_20.Total2016.sum()
conf_2017= femi15_20.Total2017.sum()
conf_2018= femi15_20.Total2018.sum()
conf_2019= femi15_20.Total2019.sum()
conf_2020= femi15_20.Total2020.sum()


#--------------------------- PREPARA GRAFICA MENSUAL
pagra = fe[[
  'Enero15', 'Febrero15', 'Marzo15', 'Abril15', 'Mayo15', 'Junio15', 'Julio15', 'Agosto15', 
    'Septiembre15', 'Octubre15', 'Noviembre15', 'Diciembre15',
 
 'Enero16', 'Febrero16', 'Marzo16', 'Abril16', 'Mayo16', 'Junio16', 'Julio16', 'Agosto16', 
    'Septiembre16', 'Octubre16', 'Noviembre16', 'Diciembre16',

 'Enero17', 'Febrero17', 'Marzo17', 'Abril17', 'Mayo17', 'Junio17', 'Julio17', 'Agosto17', 
    'Septiembre17', 'Octubre17', 'Noviembre17', 'Diciembre17', 
    'Enero18', 'Febrero18', 'Marzo18',    'Abril18', 'Mayo18', 'Junio18', 'Julio18', 'Agosto18',
    'Septiembre18', 'Octubre18', 'Noviembre18', 'Diciembre18',
 
 'Enero19', 'Febrero19', 'Marzo19', 'Abril19', 'Mayo19', 'Junio19', 'Julio19', 'Agosto19', 
    'Septiembre19', 'Octubre19', 'Noviembre19', 'Diciembre19',

 'Enero20', 'Febrero20', 'Marzo20', 'Abril20', 'Mayo20', 'Junio20', 'Julio20', 'Agosto20',
    'Septiembre20','Octubre20', 'Noviembre20', 'Diciembre20']]


pagrafm = pagra.stb.subtotal()
pagrafm.to_csv("0000procesod.csv")
#Selecciona ultima columna (Totales)
other  = pd.read_csv('0000procesod.csv')
other_s = other.iloc[32]
other_b = pd.DataFrame(other_s)
other_b.to_csv('0000procesodi.csv')
vuelve_a_abrir = pd.read_csv('0000procesodi.csv')
##Elimina filas 0 a 4 
gra_mes = vuelve_a_abrir.drop([0])
#Renombra titulo de columna
gra_mes = gra_mes.rename(columns= {"Unnamed: 0": "Mes"})
gra_mes = gra_mes.rename(columns= {"32": "Total"})
gra_mes['Total'] = pd.to_numeric(gra_mes['Total'])


#Grafica mensual 
graf_meses = go.Figure()
graf_meses.add_trace(go.Bar(x=gra_mes['Mes'],y=gra_mes['Total'],
                marker_color='indianred'  # cambiar nuemeritos de rgb
                ))
graf_meses.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45,
    template = 'simple_white',
    title='',
    xaxis_tickfont_size= 6,
    yaxis=dict(
        title='Acumulados mensuales',
        titlefont_size=14,
        tickfont_size=12,
        titlefont_family= "Monserrat"),
    #autosize=False,
    #width=1000,
    #height=400
    )





#- FILE JSON PARA ENTIDADES ------------------------------------------------------------------------------



################################################ SUMA TODOS LOS AÑOS ranking de municipios por estado (3edos)

#filtro de feminicidio
delitos.groupby(['Municipio','Entidad',])['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
                                             'Junio','Julio', 'Agosto', 'Septiembre', 'Octubre',
                                             'Noviembre', 'Diciembre'].sum().to_csv('0000procesofem.csv')

fem_filter1=pd.read_csv('0000procesofem.csv')
fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']] = fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']].astype(int)
    
fem_filter1['Total']=fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']].sum(1)




#- FILE MUNICIPIOS ------------------------------------------------------------------------------

fem_filter1.fillna(0, inplace=True) 
fem_filter1['Total']=fem_filter1['Total'].astype(int)




############################################### filtro para estados(3) e identifiación de mpios y abs feminicidios

# estado 1
estado1=fem_filter1[fem_filter1.Entidad=='México']
edo1orden=estado1[['Municipio','Total']].sort_values('Total',ascending=False)
#1
edo1mpio1=edo1orden.iloc[0]['Municipio']
edo1mpio1v=edo1orden.iloc[0]['Total']
#2
edo1mpio2=edo1orden.iloc[1]['Municipio']
edo1mpio2v=edo1orden.iloc[1]['Total']
#3
edo1mpio3=edo1orden.iloc[2]['Municipio']
edo1mpio3v=edo1orden.iloc[2]['Total']
#4
edo1mpio4=edo1orden.iloc[3]['Municipio']
edo1mpio4v=edo1orden.iloc[3]['Total']
#5
edo1mpio5=edo1orden.iloc[4]['Municipio']
edo1mpio5v=edo1orden.iloc[4]['Total']

# estado 2
estado2=fem_filter1[fem_filter1.Entidad=='Veracruz de Ignacio de la Llave']
edo2orden=estado2[['Municipio','Total']].sort_values('Total',ascending=False)
#1
edo2mpio1=edo2orden.iloc[0]['Municipio']
edo2mpio1v=edo2orden.iloc[0]['Total']
#2
edo2mpio2=edo2orden.iloc[1]['Municipio']
edo2mpio2v=edo2orden.iloc[1]['Total']
#3
edo2mpio3=edo2orden.iloc[2]['Municipio']
edo2mpio3v=edo2orden.iloc[2]['Total']
#4
edo2mpio4=edo2orden.iloc[3]['Municipio']
edo2mpio4v=edo2orden.iloc[3]['Total']
#5
edo2mpio5=edo2orden.iloc[4]['Municipio']
edo2mpio5v=edo2orden.iloc[4]['Total']

# estado 3
estado3=fem_filter1[fem_filter1.Entidad=='Ciudad de México']
edo3orden=estado3[['Municipio','Total']].sort_values('Total',ascending=False)
#1
edo3mpio1=edo3orden.iloc[0]['Municipio']
edo3mpio1v=edo3orden.iloc[0]['Total']
#2
edo3mpio2=edo3orden.iloc[1]['Municipio']
edo3mpio2v=edo3orden.iloc[1]['Total']
#3
edo3mpio3=edo3orden.iloc[2]['Municipio']
edo3mpio3v=edo3orden.iloc[2]['Total']
#4
edo3mpio4=edo3orden.iloc[3]['Municipio']
edo3mpio4v=edo3orden.iloc[3]['Total']
#5
edo3mpio5=edo3orden.iloc[4]['Municipio']
edo3mpio5v=edo3orden.iloc[4]['Total']

# estado 4
estado4=fem_filter1[fem_filter1.Entidad=='Jalisco']
edo4orden=estado4[['Municipio','Total']].sort_values('Total',ascending=False)
#1
edo4mpio1=edo4orden.iloc[0]['Municipio']
edo4mpio1v=edo4orden.iloc[0]['Total']
#2
edo4mpio2=edo4orden.iloc[1]['Municipio']
edo4mpio2v=edo4orden.iloc[1]['Total']
#3
edo4mpio3=edo4orden.iloc[2]['Municipio']
edo4mpio3v=edo4orden.iloc[2]['Total']
#4
edo4mpio4=edo4orden.iloc[3]['Municipio']
edo4mpio4v=edo4orden.iloc[3]['Total']
#5
edo4mpio5=edo4orden.iloc[4]['Municipio']
edo4mpio5v=edo4orden.iloc[4]['Total']



######################################################### tablas Ranking municipios
############## tabla 1
patabla1 = {'Mpio' : [edo1mpio1,edo1mpio2,edo1mpio3,edo1mpio4,edo1mpio5],
            'Casos': [edo1mpio1v,edo1mpio2v,edo1mpio3v,edo1mpio4v,edo1mpio5v],}

patabla1a = pd.DataFrame (patabla1, columns = ['Mpio','Casos'])


############## tabla 2
patabla2 = {'Mpio'  : [edo2mpio1,edo2mpio2,edo2mpio3,edo2mpio4,edo2mpio5],
            'Casos' : [edo2mpio1v,edo2mpio2v,edo2mpio3v,edo2mpio4v,edo2mpio5v],}

patabla2a = pd.DataFrame (patabla2, columns = ['Mpio','Casos'])


############## tabla 3
patabla3 = {'Mpio'  : [edo3mpio1,edo3mpio2,edo3mpio3,edo3mpio4,edo3mpio5],
            'Casos' : [edo3mpio1v,edo3mpio2v,edo3mpio3v,edo3mpio4v,edo3mpio5v],}

patabla3a = pd.DataFrame (patabla3, columns = ['Mpio','Casos'])


############## tabla 4
patabla4 = {'Mpio'  : [edo4mpio1,edo4mpio2,edo4mpio3,edo4mpio4,edo4mpio5],
            'Casos' : [edo4mpio1v,edo4mpio2v,edo4mpio3v,edo4mpio4v,edo4mpio5v],}

patabla4a = pd.DataFrame (patabla4, columns = ['Mpio','Casos'])
######################################################### MAPAS 3estados con más feminicidios

#concat2 = concat[concat.Entidad == "Veracruz de Ignacio de la Llave"]
#concat.plot("NOM_ENT", cmap= "Oranges", legend=True, k=5)
#plt.axis("off")
#plt.savefig("ver.png", dpi= 120)
#plt.show()


####################################

# A P P

####################################

########### Define your variables
mytitle=' '
tabtitle='Feminicidios'
sourceurl='https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva?state=published'


server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
# Cintillo 000
        dbc.Row(
           [
               dbc.Col(dbc.CardImg(src="https://github.com/fdealbam/CamaraDiputados/blob/main/application/static/logocamara.jfif?raw=true"),
                        width={'size': 1,  "offset": 1}),
               dbc.Col(html.H1("Feminicidios en México"),
                        width={'offset' : 2}),
           ]),

       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
    
#Cintillo 00    
    dbc.Row(
           [
               dbc.Col(html.H6(d2),           #Fecha de actualización
               width={'size' : "auto",
                      'offset' : 4}), 
           ]),  
    dbc.Row(
           [
               dbc.Col(html.H6("Fuente: SENSNSP"),
                        width={'size': 3,  "offset":1 }),
            ]),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
    
    
#cintillo 0
    
     dbc.Row(
           [
               dbc.Col(html.H1("Casos Anuales"),
                        width={'size': 5,  "offset":1 }),
            ]),

       html.Hr(),
       html.Hr(),
       html.Hr(),
    
     dbc.Row(
           [
               dbc.Col(html.H5("2015")),
               dbc.Col(html.H5("2016")),
               dbc.Col(html.H5("2017")),
               dbc.Col(html.H5("2018")),
               dbc.Col(html.H5("2019")),
               dbc.Col(html.H5("2020")),
           ]),#justify= "start"),
    
#Cintillo 1
    dbc.Row(
           [
               dbc.Col(html.H2(conf_2015)),
               dbc.Col(html.H2(conf_2016)),
               dbc.Col(html.H2(conf_2017)),
               dbc.Col(html.H2(conf_2018)),
               dbc.Col(html.H2(conf_2019)),
               dbc.Col(html.H2(conf_2020)),
            ]),#justify= "start"),
    
# Cintillo 1.1
        dbc.Row([
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2015.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2016.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2017.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2018.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2019.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mapa2020.jpeg?raw=true")),
           ]),
    
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       
#---------Grafica mensual
     dbc.Row(
           [
               dbc.Col(html.H1("Casos mensuales (2015-2020)"),
                        width={'size': 6,  "offset":1 }),
            ]),
   
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=graf_meses, config= "autosize")),
        ]),

       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
    
##Cintillo mapas y ranking

    #títulos
     dbc.Row(
           [
               dbc.Col(html.H1("Municipios en entidades con más casos"),
                        width={'size': 7,  "offset":1 }),
            ]),

       html.Hr(),
       html.Hr(),
       html.Hr(),
    
     dbc.Row(
           [
               dbc.Col(html.H3("México"),
                        width=4, lg={'size': 2,  "offset": 1, }),
               dbc.Col(html.H3("Veracruz"),
                        width=4, lg={'size': 1,  "offset": 3, }),
           ], justify= "center"),
    dbc.Row([
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/mx.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/cdmx.jpeg?raw=true")),
           ]),
       html.Hr(),

    ################################################################# tablas MIUNICIPIOS ranking 1-2    
    dbc.Row([
               dbc.Col(dbc.Table.from_dataframe(patabla1a, 
                        bordered="success", size=82, striped=True), 
                        width=4, lg={'size': 3,  "offset": 2, }),
        
               dbc.Col(dbc.Table.from_dataframe(patabla2a,
                        bordered="success", size=82, striped=True), 
                        width=4, lg={'size': 3,  "offset": 3, }),
            ]),

       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
    
    
    
     dbc.Row(
           [
               dbc.Col(html.H3("Ciudad de México"),
                        width=4, lg={'size': 3,  "offset": 1, }),
                      
               dbc.Col(html.H3("Jalisco"),
                        width=4, lg={'size': 1,  "offset": 4, }),
           ]),
    
    dbc.Row([
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/ver.jpeg?raw=true")),
               dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/feminicidios/blob/main/application/static/jal.jpeg?raw=true")),
           ]),
   
    
# Cintillo 3
       ##### tablas ranking 3-4
    dbc.Row([
               dbc.Col(dbc.Table.from_dataframe(patabla3a,
                        bordered="success", size=82, striped=True), 
                        width=4, lg={'size': 3,  "offset": 2, }),
    
        
               dbc.Col(dbc.Table.from_dataframe(patabla4a,
                        bordered="success", size=82, striped=True), 
                        width=4, lg={'size': 3,  "offset": 3, }),
            ]),

    
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.Hr(),
    

# nuevo
    
    dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H4("Consideraciones generales "),
                html.P(
                    "Los feminicidios son un problema aún irresuelto y son tema central de la " 
                    "agenda de seguridad nacional. La gravedad del fenómeno se observa "
                    "en los registros anual y mensual, que se presentan al "
                    "inicio de esta visualización. ",
                    className="lead"),
                html.P(
                    "Existe una mayor atención institucional y atención publica al fenómeno en los últimos "
                    "años, lo que hace que todos seamos más vigilantes al respecto. No obstante, sin duda aún "
                    "hace falta más acción social y más intervención institucional para "
                    "establecer estrategias efectivas de prevención y denuncia. "
                    , className="lead"),
                html.P(
                    "Este es un ejercicio institucional de informar a la sociedad, cuya fuente de información "
                    "es el Secretariado Ejecutivo Ejecutivo Nacional del Sistema Nacional de Seguridad Nacional "
                    "(SENSNSP, Gobierno Federal), que seguramente puede ser completado con otras fuentes de "
                    "información gubernamentales y de información proveniente de organizaciones civiles que "
                    "dan seguimiento al tema. ",className="lead"),
            ], fluid=True,
        )
    ],
    fluid=True,
    ),    
    
        
    
    
    

    dbc.Row([
                                    #https://github.com/fdealbam/CamaraDiputados/blob/b11ef31e8e0f73e1a4a06ce60402563e1bd0122e/application/static/logocamara.jfif
           dbc.Col(dbc.CardImg(src="https://github.com/fdealbam/CamaraDiputados/blob/main/application/static/logocamara.jfif?raw=true"),
                        width=4, lg={'size': 1,  "offset": 3, }),
            
           dbc.Col(html.H6(" S e c r e t a r í a   G e n e r a l," 
                           " Secretaría de Servicios Parlamentarios, "
                           " México, 2021 "),
                  width={'size': 3, 'offset': 0}),
               ], justify="start",),
        
            ])


app.layout = html.Div([body])

from application.dash import app
from settings import config

if __name__ == "__main__":
    app.run_server()
