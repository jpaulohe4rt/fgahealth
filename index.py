import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

from apps import dashboard_global, dashboard_local, referencias, sobre_nos


app.layout = html.Div(children=[
    html.Div(
        id='header',
        children=[
            html.Img(
                id='logo_1',
                src='/assets/logo_fga.png',
            ),

            html.P(
                'FGA Health Analytics',
            ),

            html.Img(
                id='logo_2',
                src='/assets/logo_fga.png',
            ),
        ]
    ),
    html.Div(
        id='navbar',
        children=[
            dcc.Link('Global', href='/apps/dashboard_global', id='navbar_global_selection'),
            dcc.Link('Local', href='/apps/dashboard_local', id='navbar_local_selection'),
            dcc.Link('Referencias', href='/apps/referencias', id='navbar_referencias_selection'),
            dcc.Link('Sobre Nós', href='/apps/sobre_nos', id='navbar_sobre_nos_selection'),
        ]
    ),
    dcc.Location(id='url', refresh=False, pathname='/apps/dashboard_global'),
    html.Div(id='page-content', children=[]),
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def dispaly_page(pathname):
    if pathname == '/apps/dashboard_global':
        return dashboard_global.layout
    
    elif pathname == '/apps/dashboard_local':
        return dashboard_local.layout

    elif pathname == '/apps/referencias':
        return referencias.layout

    elif pathname == '/apps/sobre_nos':
        return sobre_nos.layout

    else:
        return "404 Page Error! Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=True)