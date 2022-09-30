import time
import os
import dash
import pandas as pd
import base64
import plotly.graph_objects as go
from flask import Flask
from dash import Dash, Input, Output, dash_table, callback_context, State
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash.dcc import Download, send_data_frame
from flask_caching import Cache
import main_page, map_page, functions



# defining server object
server = Flask(__name__)

# defining app object
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
        }
    ] ,
)

# setting the title of the app which will be shown in browser tab
app.title='Commodities Trading Dashboard'

# setting some callbacks errors handling in the app
app.config.suppress_callback_exceptions = True

# getting the local directory of the app
app_directory = os.path.dirname(os.path.abspath(__file__))

# reading the dataset ( csv file ) from the app local directory
csv_file_directory = os.path.join(app_directory, 'commodity_trade_statistics_data.csv')

# setting the directory of caching folder
cache_directory = os.path.join(app_directory, 'cache_folder')

# setting the directory of logo image
img_file_directory=os.path.join(app_directory, 'rev.jpeg')

# creating cache object
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': cache_directory
})

# reading the csv file
dff = pd.read_csv(csv_file_directory)

# getting only the columns we are interested in with our analysis
df =dff[['country_or_area', 'year', 'commodity', 'flow', 'trade_usd', 'category']]

# setting a dictionery of 2 main colors in the dashboard
colors_dict = {'main_header': '#0f2537', 'app_bg':'#EBECF0'}

# creating the header text component on the top of the app
header_text = html.Div('Commodities Trading Dashboard',id='main_header_text',className='main_header',
                     style=dict(color='white',
                     fontWeight='bold',fontSize='', textAlign='center', display='inline-block'
                     ))

# setting the spacing of the of the header text component inside a column
header_text_col =  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=0), sm=dict(size=10,offset=0),
        md=dict(size=8,offset=0), lg=dict(size=4,offset=0), xl=dict(size=4,offset=0)
                           )

# encoding the logo image
encoded = base64.b64encode(open(img_file_directory, 'rb').read())

# creating html image component to display the logo image
logo_img=html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', height='50vh',
                  style=dict(paddingLeft='0.5vw',border=''))

logo_img = html.Div([logo_img], style=dict(display='inline-block'))

logo_img_col = dbc.Col([logo_img] ,
        xs=dict(size=2,offset=0), sm=dict(size=2,offset=0),
        md=dict(size=4,offset=0), lg=dict(size=1,offset=0), xl=dict(size=1,offset=0),
                       style=dict(border=''))

# creating pages links to be used to switch between the 2 pages
page1=html.Div( dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Main Page", active='exact', href="/page1",id='page1',className="header-link",
                                style=dict(fontSize='',textAlign=''))),

    ],pills=False )  ,style=dict(display='inline-block', paddingLeft='2vw'))

page2=html.Div( dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Map Visualization", active='exact', href="/page2",id='page2',className="header-link",
                                style=dict(fontSize='',textAlign=''))),

    ],pills=False )  ,style=dict(display='inline-block', paddingLeft='0.5vw'))


pages_links_col=dbc.Col([logo_img, page1, page2] ,
        xs=dict(size=4,offset=0), sm=dict(size=4,offset=0),
        md=dict(size=4,offset=0), lg=dict(size=5,offset=0), xl=dict(size=5,offset=0),
                        style=dict(border=''))

# wrapping all previous components inside the main header row
main_header_row = dbc.Row([pages_links_col, header_text_col]
                                   ,style=dict(backgroundColor=colors_dict['main_header'],
                                               paddingTop='0.5vh',paddingBottom='0.5vh',))

# getting the initial layout of the app ( main_page )
initial_page = main_page.get_layout(df)


# creating the dash app layout object
app.layout = html.Div([dbc.Card(main_header_row), html.Br(),
                        dbc.Spinner([html.Div([initial_page],id='page_layout')],
                                     size="lg", color="primary", id='loading',
                                  type="border", fullscreen=False, delay_show=999999,spinner_style=dict(marginTop='5vh')),
                       dcc.Location(id='url', refresh=True, pathname='/page1'),
                       html.Br(), html.Br()]
                      ,style = dict(backgroundColor=colors_dict['app_bg'])
                      ,className = 'main'
)


# callback to switch between the 2 pages upon pressing on pages links
# i used server side caching with this callback as the main page layout takes lots of time to be loaded
@app.callback([Output('page_layout', 'children'),Output('loading', 'delay_show')],
              Input('url', 'pathname')
    , prevent_initial_call=True
              )
@cache.memoize(timeout=0)
def update_page(url):
    # checking the url of the ( which changes upon pressing on page link )
    # then updating the layout depending on page url
    # the numbers returned is just a tweak i made for showing the loading sign on specific time
    if url == '/page1':
        return main_page.get_layout(df), 999999

    elif url == '/page2':
        return map_page.get_layout(df), 3000

    else:
        raise PreventUpdate


# callback to export the table data to excel file upon clicking on button
@app.callback(Output('download_excel', 'data'),
              Input('download_excel_button', 'n_clicks'),State('trade_balance_table','data')

    ,prevent_initial_call=True)
def export_to_excel(clicks,data):
    # converting the table json data to dataframe
    trade_balance_df=pd.DataFrame(data)
    # getting the dataframe from the browser and downloading it as excel file
    return send_data_frame(trade_balance_df.to_excel, "Balance_of_Trade.xlsx")


# callback to update Number of Trades figure upon changing any of its filters
@app.callback(Output('trades_num_fig', 'figure'),
              [Input('countries_menu1', 'value'), Input('categories_menu1', 'value'),
               Input('chart_type_options', 'value')]
                ,prevent_initial_call=True)
def update_trades_num_figure(selected_country, selected_category, selected_chart_type):
    # getting the original dataframe
    graph_df = df.copy()
    # getting the figure from its corresponding function in function.py file
    fig = functions.get_trades_num_figure(graph_df, selected_country, selected_category, selected_chart_type)

    return fig


# callback to update Balance of Trades figure upon changing any of its filters
@app.callback(Output('trades_balance_fig', 'figure'),
              Input('countries_menu2', 'value')
                ,prevent_initial_call=True)
def update_trades_balance_figure(selected_country):
    # getting the original dataframe
    graph_df = df.copy()
    # getting the figure from its corresponding function in function.py file
    fig = functions.get_balance_figure(graph_df, selected_country)

    return fig


# callback to update Top 20 Countries figure upon changing any of its filters
@app.callback(Output('top10_fig', 'figure'),
              Input('trades_type_options', 'value')
                ,prevent_initial_call=True)
def update_top10_figure(selected_flow):
    # getting the original dataframe
    graph_df = df.copy()
    # getting the figure from its corresponding function in function.py file
    fig = functions.get_top10_chart(graph_df, selected_flow)

    return fig


# callback to show country flow percentages and other info upon hovering on a country in the map
@app.callback(
    [Output("graph_tooltip", "show"),
     Output("graph_tooltip", "bbox"),
     Output("graph_tooltip", "children")],
    Input("map_fig", "hoverData")
, prevent_initial_call = True
)
def display_hover(hoverData):
    # if no data is hovered on, just show nothing
    if hoverData is None:
        return False, dash.no_update, dash.no_update

    # getting the map json data
    pt = hoverData["points"][0]
    # getting the coordinates of hovered point
    bbox = pt["bbox"]

    # creating a div contains a text of the country hovered on
    country_div = html.Div('Country: {}'.format(pt['location']), className='table_header',
                            style=dict(fontSize='1.4vh', fontWeight='bold', color='black',
                                       textAlign="left", width='100%'))

    # creating a div contains a text of Number of Trades of the country hovered on
    trades_div = html.Div('Number of Trades: {}'.format(pt['z']), className='table_header',
                            style=dict(fontSize='1.4vh', fontWeight='bold', color='black',
                                       textAlign="left", width='100%'))

    # filtering the original df by country hovered on and grouping by the flow
    dff = df[df['country_or_area'] == pt['location']]
    dff = dff.groupby(['flow'])['commodity'].count()

    # creating a pie chart that contains the percentages of flows of the hovered country
    pie = go.Figure(
        data=go.Pie(labels=dff.index, values=dff, #hole=.3,
                    showlegend=False, sort=False))


    pie.update_traces(hoverinfo='none', textinfo='label+percent', textfont_size=14, textfont_family='Arial',
                        marker=dict(colors=['#1500FF', '#FF8C00', '#3B98F5', '#F5D700'],
                                    line=dict(color='black')),
                        texttemplate='<b>%{label}</br></br>%{percent}</b>')

    pie.update_layout(
        font=dict(size=12, family='Arial', color='black')
        , hoverlabel=dict(font_size=12, font_family="Rockwell")
        , plot_bgcolor='white',
        paper_bgcolor='white', margin=dict(l=0, r=0, t=20, b=0)

    )

    pie_div = dcc.Graph(id='pie', config={'displayModeBar': False, 'displaylogo': False},
                  style=dict(height='22vh', backgroundColor='white', width='22vh'), figure=pie
                  )

    # creating the children list that will be shown on the hover tooltip upon hovering
    children = [country_div, html.Br(),trades_div, html.Br(), pie_div]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(host='localhost',port=8550,debug=False,dev_tools_silence_routes_logging=True)