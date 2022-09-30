import dash_bootstrap_components as dbc
from dash import dcc, html
import functions


def get_layout(df):
    # a text to inform the user that hovering shows more details
    info_text = html.Div('Hover over a country to see more info..', 
                            style=dict(fontSize='1.9vh', fontWeight='', color='black',
                                       textAlign="left", width='100%', paddingLeft='2rem'))

    # map figure part
    map_fig = functions.get_map_figure(df)
    map_graph = dcc.Graph(figure=map_fig, config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                          id='map_fig', className='map_graph',clear_on_unhover=True,
                          style=dict(width='100%', height='65vh'))

    map_graph = dbc.Spinner([map_graph], size="lg", color="primary", type="border",
                            fullscreen=False, delay_show=1000)

    graph_tooltip = dcc.Tooltip(id="graph_tooltip")

    map_card = dbc.Card([dbc.CardBody([info_text, map_graph, graph_tooltip])]
                        , style=dict(backgroundColor='white', height=''), className='shadow my-2 mx-3 css class')

    map_col = dbc.Col(map_card,
                      xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                      md=dict(size=6, offset=0), lg=dict(size=10, offset=1), xl=dict(size=10, offset=1),
                      style=dict(paddingTop=''))

    layout = dbc.Row([map_col])

    return layout


