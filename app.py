import dash

app = dash.Dash(__name__, 
    suppress_callback_exceptions=True,
    title='Fga Health Analytics', 
    update_title='Carregando...',
)
server = app.server
