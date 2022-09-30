import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dcc import Download, send_data_frame
import functions



def get_layout(df):

    # setting the styling variables of the indicators on top of the dashboard
    indicator_color = '#0096eb'
    indicator_bg_color = 'white'
    indicator_header_color = '#585660'
    indicator_card_width = '15%'

    # this part is for creating number of countries indicator div
    countries_text = html.Div(html.Div('No. Countries', className='info-header',
                                       style=dict(fontWeight='bold', color=indicator_header_color,
                                                  )),
                              style=dict(textAlign="center", width='100%'))

    countries_num = df['country_or_area'].nunique()
    countries_value = html.Div(html.H4(countries_num,
                                       style=dict(fontWeight='bold', color=indicator_color
                                                  )), className='num',
                               style=dict(textAlign="center", width='100%'))

    countries_card = dbc.Card([  # dbc.CardHeader(countries_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([countries_text,
                      dbc.Spinner([countries_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width,
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # this part is for creating years range indicator div
    years_text = html.Div(html.Div('Years Range', className='info-header',
                                   style=dict(fontWeight='bold', color=indicator_header_color,
                                              )),
                          style=dict(textAlign="center", width='100%'))

    years_range = '{} - {}'.format(df['year'].min(), df['year'].max())

    years_range_value = html.Div(html.H4(years_range,
                                         style=dict(fontWeight='bold', color=indicator_color
                                                    )), className='num',
                                 style=dict(textAlign="center", width='100%'))

    years_card = dbc.Card([  # dbc.CardHeader(years_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([years_text,
                      dbc.Spinner([years_range_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width, marginLeft='2vw',
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # this part is for creating Commodities Categories indicator div
    comm_types_text = html.Div(html.Div('Commodities Categories', className='info-header',
                                        style=dict(fontWeight='bold', color=indicator_header_color, paddingTop=0
                                                   )),
                               style=dict(textAlign="center", width='100%'))

    comm_types = df['category'].nunique()

    comm_types_value = html.Div(html.H4(comm_types,
                                        style=dict(fontWeight='bold', color=indicator_color
                                                   )), className='num',
                                style=dict(textAlign="center", width='100%'))

    comm_types_card = dbc.Card([  # dbc.CardHeader(comm_types_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([comm_types_text,
                      dbc.Spinner([comm_types_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width, marginLeft='2vw',
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # this part is for creating Commodities Products indicator div
    comm_products_text = html.Div(html.Div('Commodities Products', className='info-header',
                                           style=dict(fontWeight='bold', color=indicator_header_color,
                                                      )),
                                  style=dict(textAlign="center", width='100%'))

    comm_products = df['commodity'].nunique()

    comm_products_value = html.Div(html.H4(comm_products,
                                           style=dict(fontWeight='bold', color=indicator_color
                                                      )), className='num',
                                   style=dict(textAlign="center", width='100%'))

    comm_products_card = dbc.Card([  # dbc.CardHeader(comm_types_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([comm_products_text,
                      dbc.Spinner([comm_products_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width, marginLeft='2vw',
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # this part is for creating Total Imports indicator div
    total_imports_text = html.Div(html.Div('Total Imports', className='info-header',
                                           style=dict(fontWeight='bold', color=indicator_header_color,
                                                      )),
                                  style=dict(textAlign="center", width='100%'))

    flows_count = df['flow'].value_counts()
    total_imports = flows_count['Import'] + flows_count['Re-Import']
    total_exports = flows_count['Export'] + flows_count['Re-Export']

    total_imports_value = html.Div(html.H4(total_imports,
                                           style=dict(fontWeight='bold', color=indicator_color
                                                      )), className='num',
                                   style=dict(textAlign="center", width='100%'))

    total_imports_card = dbc.Card([  # dbc.CardHeader(comm_types_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([total_imports_text,
                      dbc.Spinner([total_imports_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width, marginLeft='2vw',
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # this part is for creating Total Exports indicator div
    total_exports_text = html.Div(html.Div('Total Exports', className='info-header',
                                           style=dict(fontWeight='bold', color=indicator_header_color,
                                                      )),
                                  style=dict(textAlign="center", width='100%'))

    total_exports_value = html.Div(html.H4(total_exports,
                                           style=dict(fontWeight='bold', color=indicator_color
                                                      )), className='num',
                                   style=dict(textAlign="center", width='100%'))

    total_exports_card = dbc.Card([  # dbc.CardHeader(comm_types_text, style=dict(backgroundColor='transparent')),
        dbc.CardBody([total_exports_text,
                      dbc.Spinner([total_exports_value], size="lg", color="primary",
                                  type="border", fullscreen=False,
                                  spinner_style=dict(marginTop=''))

                      ])]
        , style=dict(backgroundColor=indicator_bg_color, width=indicator_card_width, marginLeft='2vw',
                     border='1px solid {}'.format(indicator_color), borderRadius='1rem'), id='',
        className='info-card')

    # the column that contains all indicators cards
    indicators_column = dbc.Col([html.Div([countries_card, years_card, comm_types_card,
                                           comm_products_card, total_imports_card, total_exports_card],
                                          style=dict(display='flex', alignItems='center',
                                                     justifyContent='center', width='100%'))],
                                xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                                md=dict(size=12, offset=0), lg=dict(size=10, offset=1), xl=dict(size=8, offset=2),
                                style=dict(paddingBottom='1vh'))

    # dropdowns styling variables
    dropdowns_font = 'black'
    dropdowns_bg = '#DCDCDC'
    dropdowns_bg_radius = '5%'
    dropdowns_border = '#BEBEBE'
    dropdowns_width = '30%'

    # getting countries and categories lists to be used in dropdowns
    countries = df['country_or_area'].unique().tolist()
    comm_categories = df['category'].unique().tolist()
    comm_categories.insert(0, 'All Categories')

    # countries dropdown menu part
    countries_menu1 = dcc.Dropdown(
        options=[{'label': country, 'value': country} for country in countries],
        value=countries[0], className='dropdown_filter', multi=False,
        id='countries_menu1', clearable=False,
        style=dict(color=dropdowns_font, fontWeight='bold', textAlign='center', borderRadius=dropdowns_bg_radius,
                   width='100%', backgroundColor=dropdowns_bg, border='1px solid {}'.format(dropdowns_border))
    )

    countries_menu1_text = html.Div('Countries', className='filters_header',
                                    style=dict(fontSize='', fontWeight='bold', color='black',
                                               textAlign="center", width='100%', paddingBottom='0.5vh'))

    countries_menu1_div = html.Div([countries_menu1_text, countries_menu1],
                                   style=dict(fontSize='', display='inline-block', width=dropdowns_width))

    # categories dropdown menu part
    categories_menu1 = dcc.Dropdown(
        options=[{'label': category, 'value': category} for category in comm_categories],
        value=comm_categories[0], className='dropdown_filter',
        id='categories_menu1', clearable=False,
        style=dict(color=dropdowns_font, fontWeight='bold', textAlign='center', borderRadius=dropdowns_bg_radius,
                   width='100%', backgroundColor=dropdowns_bg, border='1px solid {}'.format(dropdowns_border))
    )

    categories_menu1_text = html.Div('Categories', className='filters_header',
                                     style=dict(fontSize='', fontWeight='bold', color='black',
                                                textAlign="center", width='100%', paddingBottom='0.5vh'))

    categories_menu1_div = html.Div([categories_menu1_text, categories_menu1],
                                    style=dict(marginLeft='2rem', marginBottom='', display='inline-block',
                                               width=dropdowns_width))

    # chart type radio buttons part
    chart_type_text = html.Div('Chart Type', className='filters_header',
                               style=dict(fontSize='', fontWeight='bold', color='black',
                                          textAlign="left", width='100%', paddingBottom='0.5vh'))

    chart_type_options = html.Div(
        [
            dbc.RadioItems(options=[{"label": "Area Chart", "value": 'Area'},
                                    {"label": "Line Chart", "value": 'Line'}, ],
                           value='Area',
                           id="chart_type_options", class_name='radio_filters',
                           inline=True, label_class_name='filter-label', input_class_name='filter-button',
                           input_checked_class_name='filter-button-checked',
                           input_style=dict(border='1px solid #0b1a50'),
                           input_checked_style=dict(backgroundColor='#0b1a50', border='1px solid #0b1a50')
                           ),
        ]
    )

    chart_type_div = html.Div([chart_type_text, chart_type_options],
                              style=dict(fontSize='', display='inline-block', marginLeft='2rem', textAlign=""))

    options1_row = html.Div([countries_menu1_div, categories_menu1_div, chart_type_div],
                            style=dict(display='flex', alignItems='center', paddingLeft='',
                                       justifyContent='center', width='100%'))

    # number of trades figure part
    trades_num_fig = functions.get_trades_num_figure(df, countries[0], comm_categories[0], 'Area')
    trades_num_graph = dcc.Graph(figure=trades_num_fig,
                                 config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                                 id='trades_num_fig', className='trades_num_graph',
                                 style=dict(width='', height=''))

    trades_num_graph = dbc.Spinner([trades_num_graph], size="lg", color="primary", type="border",
                                   fullscreen=False)

    trades_num_card = dbc.Card([dbc.CardBody([trades_num_graph, html.Hr(), options1_row])]
                               , style=dict(backgroundColor='white', height=''), className='shadow my-2 mx-3 css class')

    trades_num_col = dbc.Col([trades_num_card],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=6, offset=0), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0),
                             style=dict(paddingTop=''))

    # balance of trade figure dropdown part
    countries_menu2 = dcc.Dropdown(
        options=[{'label': country, 'value': country} for country in countries],
        value=countries[0], className='dropdown_filter', multi=False,
        id='countries_menu2', clearable=False,
        style=dict(color=dropdowns_font, fontWeight='bold', textAlign='center', borderRadius=dropdowns_bg_radius,
                   width='100%', backgroundColor=dropdowns_bg, border='1px solid {}'.format(dropdowns_border))
    )

    countries_menu2_div = html.Div([countries_menu1_text, countries_menu2],
                                   style=dict(fontSize='', display='inline-block', width=dropdowns_width))

    options2_row = html.Div([countries_menu2_div],
                            style=dict(display='flex', alignItems='center', paddingLeft='',
                                       justifyContent='center', width='100%'))

    # balance of trade figure part
    trades_balance_fig = functions.get_balance_figure(df, countries[0])
    trades_balance_graph = dcc.Graph(figure=trades_balance_fig,
                                     config={'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'pan']},
                                     id='trades_balance_fig', className='trades_balance_graph',
                                     style=dict(width='', height=''))

    trades_balance_graph = dbc.Spinner([trades_balance_graph], size="lg", color="primary", type="border",
                                       fullscreen=False)

    trades_balance_card = dbc.Card([dbc.CardBody([trades_balance_graph, html.Hr(), options2_row])]
                                   , style=dict(backgroundColor='white', height=''),
                                   className='shadow my-2 mx-3 css class')

    trades_balance_col = dbc.Col([trades_balance_card],
                                 xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                                 md=dict(size=6, offset=0), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0),
                                 style=dict(paddingTop=''))

    # flows type radio buttons part
    trades_type_text = html.Div('Flow Type', className='filters_header',
                                style=dict(fontSize='', fontWeight='bold', color='black',
                                           textAlign="left", width='100%', paddingBottom='0.5vh'))
    flows = df['flow'].unique().tolist()

    trades_type_options = html.Div(
        [
            dbc.RadioItems(options=[{'label': flow, 'value': flow} for flow in flows],
                           value=flows[0],
                           id="trades_type_options", class_name='radio_filters2',
                           inline=True, label_class_name='filter-label', input_class_name='filter-button',
                           input_checked_class_name='filter-button-checked',
                           input_style=dict(border='1px solid #0b1a50'),
                           input_checked_style=dict(backgroundColor='#0b1a50', border='1px solid #0b1a50')
                           ),
        ]
    )

    trades_type_div = html.Div([trades_type_text, trades_type_options],
                               style=dict(fontSize='', display='inline-block', marginLeft='2rem', textAlign=""))

    options3_row = html.Div([trades_type_div],
                            style=dict(display='flex', alignItems='center', paddingLeft='',
                                       justifyContent='center', width='100%'))

    # top 10 countries figure part
    top10_fig = functions.get_top10_chart(df, 'Export')
    top10_graph = dcc.Graph(figure=top10_fig, config={'displaylogo': False,
                                                      'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d',
                                                                                 'zoomIn2d', 'zoomOut2d',
                                                                                 'autoScale2d']},
                            id='top10_fig', className='trades_balance_graph',
                            style=dict(width='', height=''))

    top10_graph = dbc.Spinner([top10_graph], size="lg", color="primary", type="border",
                              fullscreen=False)

    top10_card = dbc.Card([dbc.CardBody([top10_graph, html.Hr(), options3_row])]
                          , style=dict(backgroundColor='white', height=''), className='shadow my-2 mx-3 css class')

    top10_col = dbc.Col([top10_card],
                        xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                        md=dict(size=6, offset=0), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0),
                        style=dict(paddingTop=''))

    # trades balance table part
    trades_balance_table = functions.get_trade_balance_table(df)
    trades_balance_table = dbc.Spinner([trades_balance_table], size="lg", color="primary", type="border",
                                       fullscreen=False)

    table_header = html.Div('Balance of Trade Data', className='table_header',
                            style=dict(fontSize='', fontWeight='bold', color='#302E38',
                                       textAlign="center", width='100%', paddingBottom='0.5vh'))

    # download excel part
    download_excel = html.Div([Download(id="download_excel")])

    download_excel_button = dbc.Button(
        "Export to Excel", id="download_excel_button", n_clicks=0, size='lg', className='download_excel_button',
        style=dict(fontSize='1.4vh', backgroundColor='#119DFF', color='white', fontWeight='bold', textAlign='center'))

    download_excel_div = html.Div([download_excel, download_excel_button],
                                  style=dict(paddingTop='0.5rem', display='flex', alignItems='center',
                                             justifyContent='center', width='100%'))

    trades_balance_table_card = dbc.Card([dbc.CardBody([table_header, trades_balance_table, download_excel_div])]
                                         , style=dict(backgroundColor='white', height=''),
                                         className='shadow my-2 mx-3 css class')

    trades_balance_table_col = dbc.Col([trades_balance_table_card],
                                       xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                                       md=dict(size=6, offset=0), lg=dict(size=6, offset=0), xl=dict(size=6, offset=0),
                                       style=dict(paddingTop=''))

    # wrapping all previous columns inside a row
    layout = dbc.Row([indicators_column, trades_num_col, trades_balance_col, top10_col, trades_balance_table_col])
    # returning the layout
    return layout