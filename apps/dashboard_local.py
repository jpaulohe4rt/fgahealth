import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import re
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date, datetime
import pathlib
import numpy as np
import json

from app import app

#Definindo dataframe
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df_local = pd.read_excel(DATA_PATH.joinpath("covid_brasil.xlsx"))

brazil_states = json.load(open('brazil-states.geojson', 'r'))

state_id_map = {}
for feature in brazil_states['features']:
    feature['id'] = feature['properties']['id']
    state_id_map[feature['properties']['sigla']] = feature['id']

layout = html.Div(children=[
    html.Div(
        id='pop_up_local_message', #Div utilizada para avisar usuários de seleções que não são permitidas
        children=[
            html.H1('Aviso!',
                id='title_local_pop_up',
            ),
            html.P(' ',
                id='text_local_pop_up',
            ),
        ],
        hidden=True, #Até ser alterada para False essa div não é plotada
    ),
    html.Div(
        id='block_1_local',
        children=[
            html.Div( #Div inserida dentro da secção de filtros, para lidar com o texto "O que deseja ver?"
                id='seccao_filtros_local',
                children=[
                    html.Div(
                        id = "oq_deseja_ver_local", #Texto o que deseja ver?
                        children=[
                            html.P('O que deseja ver ?'), #Como o usuário verá
                        ]
                    ),
                    html.Div( # Div inserida para colocar o texto "Gráfico 1"
                        id="grafico_1_filtro_text_local",
                        children=[
                            html.P('Gráfico 1'), #Como o usuário verá
                        ]
                    ),
                    html.Div( # Div inserida para colocar o texto "Gráfico 2"
                        id="grafico_2_filtro_text_local",
                        children=[
                            html.P('Gráfico 2'), #Como o usuário verá
                        ]
                    ),
                    
                    html.Div(
                        id='Primeira_linha_local',
                        children=[
                            dcc.Dropdown(id = 'pais_grafico_1_local',
                                options = [{'label': i, 'value': i} for i in np.sort(df_local['estado_nome'].dropna().unique())], 

                                optionHeight = 35,            #Espaço entre as opções do dropdown
                                value  = 'Acre',                #Opção padrão ao iniciar a página
                                disabled = False,             #Capacidade de interagir com o dropdown
                                multi = False,                #Permitir múltiplas escolhas 
                                searchable = True,            #Permitir digitar para procurar valor
                                placeholder = 'Selecione...', #Frase que aparece quando nada foi selecionado
                                clearable = True,             #Permitir que seja apagado o valor escolhido
                                    #classname = '',               #Extrai a calsse de algum documento css dentro da pasata assets
                                persistence = True,           #Mantem o valor até que , no type memory, a página dê um refresh
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'2.78vh',
                                    'font-size':'2vh',
                                },
                            ),

                            dcc.Dropdown(id = 'pais_grafico_2_local', #Antes grafico2_dado1
                                options = [{'label': i, 'value': i} for i in np.sort(df_local['estado_nome'].dropna().unique())], 
                                #options: Leitura da coluna location da planilha, para evitar repetição o unique
                                optionHeight = 35,
                                value  = 'Acre',
                                disabled = False,
                                multi = False,                
                                searchable = True,
                                placeholder = 'Selecione...',
                                clearable = True,
                                persistence = True,
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'2.78vh',
                                    'font-size':'2vh',
                                },
                            ),      
                        ],
                    ),

                    html.Div(
                        id='Segunda_linha_local',
                        children=[
                            dcc.Dropdown(id = 'casos_mortes_grafico_1_local',
                                options = [
                                    {'label': 'Casos', 'value':'grafico_casos' },
                                    {'label': 'Mortes', 'value': 'grafico_mortes'}], 

                                optionHeight = 35,
                                value  = ['grafico_casos', 'grafico_mortes'],
                                disabled = False,
                                multi = True,
                                searchable = False,
                                placeholder = 'Selecione...',
                                clearable = False,
                                persistence = True,
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'1.266vh',
                                    'font-size':'1.7vh',
                                },
                            ),

                            dcc.Dropdown(id = 'casos_mortes_grafico_2_local', 
                                options = [
                                    {'label': 'Casos', 'value':'grafico_casos' },
                                    {'label': 'Mortes', 'value': 'grafico_mortes'}], 

                                optionHeight = 35,
                                value  = ['grafico_casos', 'grafico_mortes'],
                                disabled = False,
                                multi = True,                
                                searchable = False,
                                placeholder = 'Selecione...',
                                clearable = False,
                                persistence = True,
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'1.266vh',
                                    'font-size':'1.7vh',
                                },
                            ),
                        ],
                    ),
                    
                    html.Div(
                        id='terceira_linha_local',
                        children=[
                            dcc.Dropdown(id = 'tipo_grafico_1_local',
                                options = [
                                    {'label': 'Barra', 'value':'grafico_barra' },
                                    {'label': 'Linha', 'value': 'grafico_linha'},
                                    {'label': 'Mapa', 'value': 'grafico_mapa'}
                                ], 

                                optionHeight = 35,
                                value  = 'grafico_barra',
                                disabled = False, 
                                multi = False,
                                searchable = False,
                                placeholder = 'Selecione...',
                                clearable = False,
                                persistence = True,
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'1.266vh',
                                    'font-size':'2vh',
                                },
                            ),

                            dcc.Dropdown(id = 'tipo_grafico_2_local',
                                options = [
                                    {'label': 'Barra', 'value':'grafico_barra' },
                                    {'label': 'Linha', 'value': 'grafico_linha'},
                                    {'label': 'Mapa', 'value': 'grafico_mapa'}
                                ], 

                                optionHeight = 35,
                                value  = 'grafico_barra',
                                disabled = False, 
                                multi = False,
                                searchable = False,
                                placeholder = 'Selecione...',
                                clearable = False,
                                persistence = True,
                                persistence_type = 'memory',
                                style={
                                    'margin-top':'1.266vh',
                                    'font-size':'2vh',
                                },
                            ),
                        ],
                    ),
                    
                    html.Div(
                        id='filtros_gerais_text_local',
                        children=[
                            html.P('Filtros Gerais'),
                        ],
                    ),

                    html.Div(
                        id='Quarta_linha_local', 
                        style={
                            'fontSize':'1px',
                        },
                        children=[
                            dcc.DatePickerRange(
                                id='escolha_data_local',
                                min_date_allowed=datetime(2020, 3, 19),
                                max_date_allowed=datetime(2020, 11, 21),
                                start_date=datetime(2020, 3, 19).date(),
                                end_date=datetime(2020, 11, 21).date(),
                                clearable=True,
                                start_date_placeholder_text="Data Inicial",
                                end_date_placeholder_text="Data Final",
                                display_format="DD/MM/YYYY",
                                minimum_nights=2,
                                persistence=True,
                                persisted_props=['start_date', 'end_date'],
                                persistence_type="session",
                            ),
                            html.Div(id='output-container-date-picker-range_local'),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.Button(
                                'GO!',
                                id='Submit_button_local',
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                id='top_3_local',
                children=[
                    dcc.Graph(
                        id='top3_local',
                        config={
                            'displayModeBar': False,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': [
                                'zoom2d', 'pan2d', 'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d',
                                'toggleSpikelines',
                            ],
                        },
                        style = {'border-radius': 30,},
                    ),
                ],
            ),
        ]
    ),

    html.Div( #Bloco de divs da direita --> Resumo geral, grafico 1 e grafico 2.
        className='resumo_geral_local',
        children=[
            html.Div(
                id='resumo_casos_local',
                children=[
                    html.Div(
                        id='icon_circle_casos_local',
                    ),

                    html.Img(
                        id='icon_casos_local',
                        src='../assets/icone_casos.svg',
                    ),

                    html.P(
                        'Casos Confirmados',
                        id='casos_confirmados_text_local',
                    ),

                    html.P(
                        'Acumulado',
                        id='acumulado_casos_text_local',
                    ),

                    html.P(
                        'Novos Casos',
                        id='novos_casos_text_local',
                    ),
                ],
            ),
            html.Div(
                id='resumo_obitos_local',
                children=[
                    html.Div(
                        id='icon_circle_obitos_local',
                    ),

                    html.Img(
                        id='icon_obitos_local',
                        src='/assets/icon_deaths.svg',
                    ),

                    html.P(
                        'Óbitos Confirmados',
                        id='obitos_confirmados_local',
                    ),

                    html.P(
                        'Acumulado',
                        id='acumulado_obitos_text_local',
                    ),

                    html.P(
                        'Letalidade',
                        id='letalidade_text_local',
                    ),

                    html.P(
                        'Novos Óbitos',
                        id='novos_obitos_text_local'
                    ),
                ],
            ),

            html.Div(
                id='grafico_1_local',
                children=[
                    dcc.Graph(
                        id='grafico-1_local',
                        config={
                            'displaylogo': False,
                            'modeBarButtonsToRemove':[
                                'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d',
                                'toggleSpikelines',
                            ],
                        }, 
                    ),
                ],
            ),

            html.Div(
                id='grafico_2_local',
                children=[
                    dcc.Graph(
                        id='grafico-2_local',
                        config={
                            'displaylogo': False,
                            'modeBarButtonsToRemove':[
                                'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d',
                                'toggleSpikelines',
                            ],
                        }, 
                    ),
                ],
            ),
        ],
    ),

])

data = 3
total_cases = 4
total_deaths = 6

def arredondamento (number):
    if number < 1000 and number > 500:
        number = int(round(number/1000.0, 1) * 1000)

    elif number < 10000 and number > 1000:
        number = int(round(number/10000.0, 1) * 10000)

    elif number < 100000 and number > 10000:
        number = int(round(number/100000.0, 1) * 100000)

    elif number < 1000000 and number > 100000:
        number = int(round(number/1000000.0, 1) * 1000000)
    
    elif number < 10000000 and number > 1000000:
        number = int(round(number/10000000.0, 1) * 10000000)
    
    elif number > 10000000:
        number = int(round(number/10000000.0, 1) * 10000000)
    
    return number

@app.callback(
Output('grafico-1_local', 'figure'),
Input('Submit_button_local', 'n_clicks'), 
[State('pais_grafico_1_local', 'value'),
State('casos_mortes_grafico_1_local', 'value'),
State('escolha_data_local', 'start_date'),
State('escolha_data_local', 'end_date'),
State('tipo_grafico_1_local', 'value'),]) #primeiro o id do dropdown q será utilizado, dps a propriedade q será mudada.
def update_figure1_local(confirm_action, selected_location, selected_info, start_date, end_date, selected_graph):
    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%Y-%m-%d')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%Y-%m-%d')

    #Restrição do dataframe
    newlocation_df1 = df_local[df_local.estado_nome == selected_location]
    new_end_date_df1 = df_local[df_local.data == end_date_string]
    
    dataframe_mapa_local = new_end_date_df1.dropna(subset = ['estado'])
    dataframe_mapa_local['id'] = dataframe_mapa_local['estado'].apply(lambda x: state_id_map[x])

    df_data_interval = newlocation_df1
    df_data_interval['data'] = df_data_interval['data'].dt.strftime('%Y-%m-%d')
    df_data_interval = df_data_interval.values.tolist()
    
    for i in range(len(df_data_interval)):
        if df_data_interval[i][data] == start_date_string:
            aux_start_date = i
    
        elif df_data_interval[i][data] == end_date_string:
            aux_end_date = i
    
    df_data_interval_update = []
    for i in range(len(df_data_interval)):
        if i >= aux_start_date and i <= aux_end_date:
            df_data_interval_update.append(df_data_interval[i])

    lista_casos = new_end_date_df1['casosAcumulado'].dropna().values.tolist()
    lista_mortes = new_end_date_df1['obitosAcumulado'].dropna().values.tolist()

    for i in range(len(lista_casos)):
        for h in range(0, len(lista_casos)-i-1 ):
            if lista_casos[h] < lista_casos[h+1]:
                lista_casos[h], lista_casos[h+1] = lista_casos[h+1], lista_casos[h]

    for i in range(len(lista_mortes)):
        for h in range(0, len(lista_mortes)-i-1 ):
            if lista_mortes[h] < lista_mortes[h+1]:
                lista_mortes[h], lista_mortes[h+1] = lista_mortes[h+1], lista_mortes[h]
    
    valor_max_casos = arredondamento(lista_casos[1])
    valor_max_mortes = arredondamento(lista_mortes[1])

    #Se a opção de tipo de informação ou tipo de localização estiver vazia, impedir atualização do gráfico 1
    if not selected_info or not selected_location: 
        raise PreventUpdate

    elif selected_graph == "grafico_barra":
        
        if selected_info == ['grafico_casos'] :

            fig_bar_local_1 = go.Figure( data = [go.Bar( 
                y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                marker =  dict(
                    autocolorscale = True,
                    color = 'rgb(255, 220, 0)',
                    line = dict(
                        color = 'black',
                        width = 1,
                    ),
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>",    
            )])
            fig_bar_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                xaxis={
                    'tickformat': '%m/%Y',
                },
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_1  #devolvendo os gráficos que o usuario pediu no imput

        elif selected_info == ['grafico_mortes'] :
            
            fig_bar_local_1 = go.Figure( data = [go.Bar(
                y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                marker =  dict(
                    autocolorscale = True,
                    color = 'rgb(255, 72, 0)',
                    line = dict(
                        color = 'black',
                        width = 1,
                    ),
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>",    
            )])

            fig_bar_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                xaxis={
                    'tickformat': '%m/%Y',
                },
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_1 #devolvendo os gráficos que o usuario pediu no imput

        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            
            fig_bar_local_1 = go.Figure( data = [
                go.Bar(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    marker =  dict(
                        autocolorscale = True,
                        color = 'rgb(255, 220, 0)',
                        line = dict(
                            color = 'black',
                            width = 1,
                        ),
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>",  
                ),
                go.Bar(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    marker = dict(
                        autocolorscale = True,
                        color = 'rgb(255, 72, 0)',
                        line = dict(
                            color = 'black',
                            width = 1,
                        ), 
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])

            fig_bar_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_1

    
    elif selected_graph == "grafico_linha":
        
        if selected_info == ['grafico_casos']:
            
            fig_scatter_local_1 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 220, 0)",
                        width = 4,
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>", 
                ),
            ])
            fig_scatter_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_1
        
        elif selected_info == ['grafico_mortes']:
            fig_scatter_local_1 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 72, 0)",
                        width = 4,
                    ),
                    mode = "lines",
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])

            fig_scatter_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_1

        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            
            fig_scatter_local_1 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 220, 0)",
                        width = 4,
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>", 
                ),

                go.Scatter(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 72, 0)",
                        width = 4,
                    ),
                    mode = "lines",
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])
            fig_scatter_local_1.update_layout(
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_1


    elif selected_graph == "grafico_mapa":

        if selected_info == ['grafico_casos']:
            fig_map_local_1 = go.Figure(data=go.Choropleth(
                locations = dataframe_mapa_local['id'], 
                z =  dataframe_mapa_local['casosAcumulado'],  
                zmax = valor_max_casos,
                zmin = 0,
                text = dataframe_mapa_local['estado_nome'],
                colorscale = [[0, 'rgb(255, 250, 173)'], [1, 'rgb(255,220,0)']],
                autocolorscale = False,
                reversescale = False,
                marker_line_color = 'black',
                marker_line_width = 0.5,
                colorbar = dict(
                    bordercolor = "black",
                    borderwidth = 1,
                    tickmode = "auto",
                    nticks = 10,
                    x = 0.8,
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                geojson = brazil_states,
                hovertemplate = " Estado: %{text} <br> Casos: %{z} <extra></extra>",
            ))

            fig_map_local_1.update_geos(
                fitbounds = 'locations',
                visible=False,)

            fig_map_local_1.update_layout(
                title_text = 'Casos de COVID-19',
                geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection_type = 'natural earth',
                    bgcolor = "#C5D5FD",
                    scope = 'south america',
                ),
                title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            )


            return fig_map_local_1

        elif selected_info == ['grafico_mortes']:
            fig_map_local_1 = go.Figure(data=go.Choropleth(
                locations = dataframe_mapa_local['id'], 
                z =  dataframe_mapa_local['obitosAcumulado'],  
                zmax = valor_max_mortes,
                zmin = 0,
                text = dataframe_mapa_local['estado_nome'],
                colorscale = [[0, 'rgb(250, 127, 114)'], [1, 'rgb(139, 0, 0)']],
                autocolorscale = False,
                reversescale = False,
                marker_line_color = 'black',
                marker_line_width = 0.5,
                colorbar = dict(
                    bordercolor = "black",
                    borderwidth = 1,
                    tickmode = "auto",
                    nticks = 10,
                    x = 0.8,
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                geojson = brazil_states,
                hovertemplate = " Estado: %{text} <br> Óbitos: %{z} <extra></extra>",
            ))

            fig_map_local_1.update_geos(
                fitbounds = 'locations',
                visible=False,)

            fig_map_local_1.update_layout(
                title_text = 'Casos de COVID-19',
                geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection_type = 'natural earth',
                    bgcolor = "#C5D5FD",
                    scope = 'south america',
                ),
                 title={
                    'text':'Gráfico 1',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            )

            return fig_map_local_1
        
        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            raise PreventUpdate


#EM PROCESSO DE TESTE DE INTEGRAÇÃO DE DATA NO GRÁFICO
@app.callback(
Output('grafico-2_local', 'figure'),
Input('Submit_button_local', 'n_clicks'), 
[State('pais_grafico_2_local', 'value'),
State('casos_mortes_grafico_2_local', 'value'),
State('escolha_data_local', 'start_date'),
State('escolha_data_local', 'end_date'),
State('tipo_grafico_2_local', 'value'),]) #primeiro o id do dropdown q será utilizado, dps a propriedade q será mudada.
def update_figure_2_local(confirm_action, selected_location, selected_info, start_date, 
                    end_date, selected_graph):

    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%Y-%m-%d')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%Y-%m-%d')

    newlocation_df1 = df_local[df_local.estado_nome == selected_location] #redefinindo o dataframe
    new_end_date_df1 = df_local[df_local.data == end_date_string]

    dataframe_mapa_local = new_end_date_df1.dropna(subset = ['estado'])
    dataframe_mapa_local['id'] = dataframe_mapa_local['estado'].apply(lambda x: state_id_map[x])

    df_data_interval = newlocation_df1
    df_data_interval['data'] = df_data_interval['data'].dt.strftime('%Y-%m-%d')
    df_data_interval = df_data_interval.values.tolist()
    
    for i in range(len(df_data_interval)):
        if df_data_interval[i][data] == start_date_string:
            aux_start_date = i
    
        elif df_data_interval[i][data] == end_date_string:
            aux_end_date = i
    
    df_data_interval_update = []
    for i in range(len(df_data_interval)):
        if i >= aux_start_date and i <= aux_end_date:
            df_data_interval_update.append(df_data_interval[i])

    lista_casos = new_end_date_df1['casosAcumulado'].dropna().values.tolist()
    lista_mortes = new_end_date_df1['obitosAcumulado'].dropna().values.tolist()

    for i in range(len(lista_casos)):
        for h in range(0, len(lista_casos)-i-1 ):
            if lista_casos[h] < lista_casos[h+1]:
                lista_casos[h], lista_casos[h+1] = lista_casos[h+1], lista_casos[h]

    for i in range(len(lista_mortes)):
        for h in range(0, len(lista_mortes)-i-1 ):
            if lista_mortes[h] < lista_mortes[h+1]:
                lista_mortes[h], lista_mortes[h+1] = lista_mortes[h+1], lista_mortes[h]
    
    valor_max_casos = arredondamento(lista_casos[1])
    valor_max_mortes = arredondamento(lista_mortes[1])

    if not selected_info or not selected_location:
        raise PreventUpdate

    elif selected_graph == "grafico_barra":
        
        if selected_info == ['grafico_casos'] :

            fig_bar_local_2 = go.Figure( data = [go.Bar( 
                y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                marker =  dict(
                    autocolorscale = True,
                    color = 'rgb(255, 220, 0)',
                    line = dict(
                        color = 'black',
                        width = 1,
                    ),
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>",    
            )])
            fig_bar_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_2  #devolvendo os gráficos que o usuario pediu no imput

        elif selected_info == ['grafico_mortes'] :
            fig_bar_local_2 = go.Figure( data = [go.Bar(
                y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                marker =  dict(
                    autocolorscale = True,
                    color = 'rgb(255, 72, 0)',
                    line = dict(
                        color = 'black',
                        width = 1,
                    ),
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>",    
            )])

            fig_bar_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_2 #devolvendo os gráficos que o usuario pediu no imput

        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            fig_bar_local_2 = go.Figure( data = [
                go.Bar(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    marker =  dict(
                        autocolorscale = True,
                        color = 'rgb(255, 220, 0)',
                        line = dict(
                            color = 'black',
                            width = 1,
                        ),
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Casos: %{y} <extra></extra>",  
                ),
                go.Bar(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    marker = dict(
                        autocolorscale = True,
                        color = 'rgb(255, 72, 0)',
                        line = dict(
                            color = 'black',
                            width = 1,
                        ), 
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x|%d/%m/%Y} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])

            fig_bar_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_bar_local_2 #devolvendo os gráficos que o usuario pediu no imput
    
    elif selected_graph == "grafico_linha":
        
        if selected_info == ['grafico_casos']:
            fig_scatter_local_2 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 220, 0)",
                        width = 4,
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x} <br> Casos: %{y} <extra></extra>", 
                ),
            ])
            fig_scatter_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_2
        
        elif selected_info == ['grafico_mortes']:
            fig_scatter_local_2 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 72, 0)",
                        width = 4,
                    ),
                    mode = "lines",
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])

            fig_scatter_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_2

        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            fig_scatter_local_2 = go.Figure( data = [
                go.Scatter(
                    y = [df_data_interval_update[i][total_cases] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 220, 0)",
                        width = 4,
                    ),
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x} <br> Casos: %{y} <extra></extra>", 
                ),

                go.Scatter(
                    y = [df_data_interval_update[i][total_deaths] for i in range(len(df_data_interval_update))],
                    x = [df_data_interval_update[i][data] for i in range(len(df_data_interval_update))],
                    line = dict(
                        color = "rgb(255, 72, 0)",
                        width = 4,
                    ),
                    mode = "lines",
                    hoverlabel = dict(
                        bgcolor = '#C5D5FD',
                        bordercolor = 'black',
                        font = dict(
                            family = 'Courier New',
                            color = 'black',
                        ),
                    ),
                    hovertemplate = " Data: %{x} <br> Óbitos: %{y} <extra></extra>", 
                ),
            ])
            fig_scatter_local_2.update_layout(
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis={
                    'tickformat': '%m/%Y',
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            ),

            return fig_scatter_local_2

    elif selected_graph == "grafico_mapa":

        if selected_info == ['grafico_casos']:
            fig_map_local_2 = go.Figure(data=go.Choropleth(
                locations = dataframe_mapa_local['id'], 
                z =  dataframe_mapa_local['casosAcumulado'],  
                zmax = valor_max_casos,
                zmin = 0,
                text = dataframe_mapa_local['estado_nome'],
                colorscale = [[0, 'rgb(255, 250, 173)'], [1, 'rgb(255,220,0)']],
                autocolorscale = False,
                reversescale = False,
                marker_line_color = 'black',
                marker_line_width = 0.5,
                colorbar = dict(
                    bordercolor = "black",
                    borderwidth = 1,
                    tickmode = "auto",
                    nticks = 10,
                    x = 0.8,
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                geojson = brazil_states,
                hovertemplate = " Estado: %{text} <br> Casos: %{z} <extra></extra>",
            ))

            fig_map_local_2.update_geos(
                fitbounds = 'locations',
                visible=False,)

            fig_map_local_2.update_layout(
                title_text = 'Casos de COVID-19',
                geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection_type = 'natural earth',
                    bgcolor = "#C5D5FD",
                    scope = 'south america',
                ),
                title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            )


            return fig_map_local_2

        elif selected_info == ['grafico_mortes']:
            fig_map_local_2 = go.Figure(data=go.Choropleth(
                locations = dataframe_mapa_local['id'], 
                z =  dataframe_mapa_local['obitosAcumulado'],  
                zmax = valor_max_mortes,
                zmin = 0,
                text = dataframe_mapa_local['estado_nome'],
                colorscale = [[0, 'rgb(250, 127, 114)'], [1, 'rgb(139, 0, 0)']],
                autocolorscale = False,
                reversescale = False,
                marker_line_color = 'black',
                marker_line_width = 0.5,
                colorbar = dict(
                    bordercolor = "black",
                    borderwidth = 1,
                    tickmode = "auto",
                    nticks = 10,
                    x = 0.8,
                ),
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                geojson = brazil_states,
                hovertemplate = " Estado: %{text} <br> Óbitos: %{z} <extra></extra>",
            ))

            fig_map_local_2.update_geos(
                fitbounds = 'locations',
                visible=False,)

            fig_map_local_2.update_layout(
                title_text = 'Casos de COVID-19',
                geo = dict(
                    showframe = False,
                    showcoastlines = False,
                    projection_type = 'natural earth',
                    bgcolor = "#C5D5FD",
                    scope = 'south america',
                ),
                 title={
                    'text':'Gráfico 2',
                    'font.size': 22,
                    'x': 0.5,
                    'y': 0.97,
                },
                xaxis_tickangle=-30,
                font_family="Courier New",
                font_size=12,
                barmode='overlay',
                margin=dict(
                    l=25,
                    r=25,
                    b=25,
                    t=45,  
                ),
                showlegend=False,
                plot_bgcolor = "#C5D5FD",
            )

            return fig_map_local_2

        elif (selected_info == ['grafico_casos', 'grafico_mortes'] or ['grafico_mortes', 'grafico_casos']):
            raise PreventUpdate

#Callback com erro por causa da data - Datas menores que 10.
@app.callback(
    Output('top3_local', 'figure'),
    Input('Submit_button_local', 'n_clicks'),
    State('escolha_data_local', 'end_date'),
)
def update_top_3_local(confirm_action, end_date):
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%Y-%m-%d')
    new_end_date_df1 = df_local[df_local.data == end_date_string]
   
    df_local_top3 = new_end_date_df1[['estado_nome','obitosAcumulado']].sort_values( by=['obitosAcumulado'],ascending=False).query('estado_nome != "Brasil"').dropna().head(3)
                                                                                                                                            
    if not end_date:
        raise PreventUpdate

    else:
        fig_bar_local_top3 = go.Figure( data = [
            go.Bar(
                x= df_local_top3['estado_nome'], 
                y = df_local_top3['obitosAcumulado'],
                textposition = 'auto',
                marker =  dict(
                    autocolorscale = True,
                    color = 'rgb(255, 72, 0)',
                    line = dict(
                        color = 'black',
                        width = 2,
                    ),
                ),        
                hoverlabel = dict(
                    bgcolor = '#C5D5FD',
                    bordercolor = 'black',
                    font = dict(
                        family = 'Courier New',
                        color = 'black',
                    ),
                ),
                hovertemplate = " País: %{x} <br> Óbitos: %{y} <extra></extra>", 
            ),
        ])
        fig_bar_local_top3.update_layout(
            title={
                'text':'Top 3',
                'font.size': 22,
                'x': 0.5,
                'y': 0.97,
            },
            xaxis_tickangle=-15,
            font_family="Courier New",
            font_size=12,
            margin=dict(
                l=25,
                r=25,
                b=10,
                t=45,  
            ),
            showlegend=False,
            plot_bgcolor = "#C5D5FD",
        ),

        return fig_bar_local_top3

@app.callback(
    [Output('pop_up_local_message', 'hidden'),
    Output('text_local_pop_up', 'children')],
    Input('Submit_button_local', 'n_clicks'),
    [State('pais_grafico_1_local', 'value'),
    State('tipo_grafico_1_local', 'value'),
    State('casos_mortes_grafico_1_local', 'value'),
    State('pais_grafico_2_local', 'value'),
    State('tipo_grafico_2_local', 'value'),
    State('casos_mortes_grafico_2_local', 'value')]
)
def pop_up_message(confirm_action, selected_location, selected_graph, selected_info, 
                    selected_location_2, selected_graph_2, selected_info_2):

    if selected_graph == "grafico_mapa" and selected_graph_2 == "grafico_mapa":
        if not selected_info or not selected_info_2:
            return False, 'Não é possível gerar gráficos com a opção tipo de informação vazia. Selecione casos, morte ou ambos e tente novamente.'
        
        elif selected_info == ['grafico_casos', 'grafico_mortes'] or selected_info_2 == ['grafico_casos', 'grafico_mortes']:
            return False, 'O gráfico de mapa não pode receber as informações de morte e casos simultaneamente. Selecione casos ou mortes, ou altere o tipo de gráfico e tente novamente.'

        else:
            return True, '...'

    if selected_graph_2 == "grafico_mapa":
        if selected_info_2 == ['grafico_casos', 'grafico_mortes']:
            return False, 'O gráfico de mapa não pode receber as informações de morte e casos simultaneamente. Selecione casos ou mortes, ou altere o tipo de gráfico e tente novamente.'
        
        elif selected_info_2 == ['grafico_casos'] or ['grafico_mortes']:
            return True, '...'

        else:
            return False, 'Não é possível gerar gráficos com a opção tipo de informação vazia. Selecione casos, morte ou ambos e tente novamente.' 

    if selected_graph == "grafico_mapa":
        if selected_info == ['grafico_casos', 'grafico_mortes']:
            return False, 'O gráfico de mapa não pode receber as informações de morte e casos simultaneamente. Selecione casos ou mortes, ou altere o tipo de gráfico e tente novamente.'

        elif selected_info == ['grafico_casos'] or ['grafico_mortes']:
            return True, '...'
        
        elif not selected_info_2 or selected_info:
            return False, 'Não é possível gerar gráficos com a opção tipo de informação vazia. Selecione casos, morte ou ambos e tente novamente.'

    elif((not selected_location or not selected_location_2) and (not selected_info or not selected_info_2)):
        return False, 'Não é possível gerar gráficos com as opções localização e tipo de informação vazias. Selecione uma localização e um tipo de informação e tente novamente.' 
    
    elif (not selected_location or not selected_location_2):
        return False, 'Não é possível gerar gráficos com a opção localização vazia. Selecione uma localização e tente novamente.'

    elif (not selected_info or not selected_info_2):
        return False, 'Não é possível gerar gráficos com a opção tipo de informação vazia. Selecione casos, morte ou ambos e tente novamente.'

    else:
        return True, '...'

@app.callback(
[Output('acumulado_casos_text_local', 'children'), 
Output('novos_casos_text_local', 'children'),
Output('acumulado_obitos_text_local', 'children'), 
Output('novos_obitos_text_local', 'children'), 
Output('letalidade_text_local', 'children')],
Input('Submit_button_local', 'n_clicks'),
[State('escolha_data_local', 'start_date'),
State('escolha_data_local', 'end_date'),]
)
def resumo_geral(confirm_action, start_date, end_date):
    
    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%Y-%m-%d')
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%Y-%m-%d')

    newlocation_df1 = df_local[df_local['regiao'] == 'Brasil']
    data_resumo_geral_fim = newlocation_df1[newlocation_df1['data'] == end_date_string]
    data_resumo_geral_inicio = newlocation_df1[newlocation_df1['data'] == start_date_string]
    
    var_resumo_casos_fim  = float(data_resumo_geral_fim['casosAcumulado'].values)
    var_resumo_casos_inicio = float(data_resumo_geral_inicio['casosAcumulado'].values)
    var_resumo_mortes_fim  = float(data_resumo_geral_fim['obitosAcumulado'].values)
    var_resumo_mortes_inicio = float(data_resumo_geral_inicio['obitosAcumulado'].values)

    children_casos_acumulado =  'Acumulado: {}'.format(var_resumo_casos_fim)
    children_casos_novos = 'Novos casos: {}'.format(var_resumo_casos_fim - var_resumo_casos_inicio)
    children_mortes_acumulado = 'Acumulado: {}'.format(var_resumo_mortes_fim)
    children_mortes_novos = 'Novos óbitos: {}'.format(var_resumo_mortes_fim - var_resumo_mortes_inicio)
    children_letalidade = 'Letalidade: {:.2f}%'.format(var_resumo_mortes_fim*100/var_resumo_casos_fim)

    return [children_casos_acumulado, children_casos_novos, children_mortes_acumulado, children_mortes_novos, children_letalidade]