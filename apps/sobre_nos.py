import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from app import app
 
layout = html.Div(children=[
    html.Img(
        id="sobre_nos_icon",
        src="../assets/sobre_nos_icon.svg",
    ),
    html.Div(
        id="background_sobre_nos",
        children=[
            html.Div(
                id="unb_gama",
                children=[
                    html.Img(
                        src="../assets/unb_gama.jpg",
                    ),
                ],
            ),
            html.Div(id="slideshow-container", 
                children=[
                    html.Img(
                        id="carrossel_imagem",
                        src='../assets/Card_Davi.png',
                    ),
                    dcc.Interval(id='interval', interval= 5000),       
                ],
            ),
            html.Div(
                id="unb",
                children=[
                    html.Img(
                        src="../assets/unb.png",
                    ),
                ],
            ),
            html.Div(
                    id='sobre_nos_texto',
                    children=[
                        html.P('Esse é o projeto FGA Health Analytics, construído pela equipe de saúde da matéria de Algoritmo e Programação de Computadores.'),
                        html.P('Nosso projeto tem a função de difundir de maneira mais rápida e precisa, as informações dessa pandemia, para que todos possam em poucos toques entender o cenário global e nacional dessa pandemia.'),
                        html.P('Está preparado para entender a situação dessa pandemia? Caso queira verificar os relatórios de covid acesse nossa aba de referências e lá poderá baixar os relatórios.'),
                    ],
                ),
            ],
        ),
    ]
)
 
@app.callback(Output('carrossel_imagem', 'src'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 10 == 9:
        return '../assets/Card_Rafael.png'
    elif n % 10 == 8:
        return '../assets/Card_Mauricio.png'
    elif n % 10 == 7:
        return '../assets/Card_Mateus.png'
    elif n % 10 == 6:
        return '../assets/Card_Marcos.png'
    elif n % 10 == 5:
        return '../assets/Card_Lavynia.png'
    elif n % 10 == 4:
        return '../assets/Card_Lara.png'
    elif n % 10 == 3:
        return '../assets/Card_Juan.png'
    elif n % 10 == 2:
        return '../assets/Card_JoaoPaulo.png'
    elif n % 10 == 1:
        return '../assets/Card_Joao.png'
    elif n % 10 == 0:
        return '../assets/Card_Davi.png'
    else:
        return None