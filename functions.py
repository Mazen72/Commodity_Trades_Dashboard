import pandas as pd
import plotly.graph_objects as go
from dash import dash_table


# a function to return number of trades figure depending on the filters selected
def get_trades_num_figure(df, selected_country, selected_category, selected_chart_type):
    # a dictionery with the flows types colors
    flow_colors = {'Export': '#1500FF', 'Re-Export': '#3B98F5', 'Import': '#FF8C00', 'Re-Import': '#F5D700'}
    # filtering by country
    df = df[df['country_or_area'] == selected_country]
    # filtering by category in case All Categories not chosen
    if selected_category != 'All Categories':
        df = df[df['category'] == selected_category]

    # grouping by year and flow
    df = df.groupby(['year', 'flow'])['commodity'].count()
    df = df.reset_index()

    # changing the figure type depending on type selected
    selected_type = ''
    if selected_chart_type == 'Area':
        selected_type = 'one'

    # looping through all flow types to create the corresponding chart
    fig = go.Figure()
    for flow in df['flow'].unique():
        graph_df = df[df['flow'] == flow]
        fig.add_trace(
            go.Scatter(x=graph_df['year'], y=graph_df['commodity'].astype('int64'), mode='lines', name=flow,
                       marker_color=flow_colors[flow]
                        , stackgroup=selected_type
                       ))

    # adjusting the xaxis scaling depending on number of years available
    if len(df['year'].unique().tolist()) <= 12:
        dtick_value = 1

    else:
        dtick_value = 2

    # styling the figure layout
    fig.update_layout(title = '<b>Number of Trades Over Years<b>', title_x=0.5,
        xaxis_title='<b>Years<b>', yaxis_title='<b>Number of Trades<b>',
        font=dict(size=12, family='Arial', color='black'), hoverlabel=dict(
            font_size=16, font_family="Rockwell", #font_color='black', bgcolor='white'
        ), plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            dtick=dtick_value,
            tickwidth=2, #tickcolor='#80ced6',
            ticks="outside",
            tickson="labels",
            rangeslider_visible=False
        ), margin=dict(l=0, r=0, t=30, b=0)
    )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black')
    return fig


# a function to return balance of trades figure depending on the filters selected
def get_balance_figure(df, selected_country):
    # filtering by country
    df = df[df['country_or_area'] == selected_country]

    # grouping by year and flow
    df = df.groupby(['year', 'flow'])['trade_usd'].sum()
    df = df.reset_index()
    # getting years list
    years = df['year'].unique().tolist()

    # looping through all years to get balance of trades ( Total Exports - Total Imports )
    trades_balance = []
    # looping through years
    for year in years:
        # getting sum of exports of that year
        filtered_df = df[df['year'] == year]

        exports_df = filtered_df[filtered_df['flow'] == 'Export']
        if exports_df.empty:
            exports = 0
        else:
            exports = exports_df['trade_usd'].values[0]

        # getting sum of imports of that year
        imports_df = filtered_df[filtered_df['flow'] == 'Import']
        if imports_df.empty:
            imports = 0
        else:
            imports = imports_df['trade_usd'].values[0]

        # getting sum of re-exports of that year
        re_exports_df = filtered_df[filtered_df['flow'] == 'Re-Export']
        if re_exports_df.empty:
            re_exports = 0
        else:
            re_exports = re_exports_df['trade_usd'].values[0]

        # getting sum of re-imports of that year
        re_imports_df = filtered_df[filtered_df['flow'] == 'Re-Import']
        if re_imports_df.empty:
            re_imports = 0
        else:
            re_imports = re_imports_df['trade_usd'].values[0]

        # getting balance of trade
        trade_balance = (exports + re_exports) - (imports + re_imports)
        # appending to the list
        trades_balance.append(round(trade_balance,2))

    # creating the chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=years, y=trades_balance, mode='lines', name=selected_country,
                   marker_color='#0096eb'
                   ))

    if len(years) <= 12:
        dtick_value = 1

    else:
        dtick_value = 2

    fig.update_layout(title = '<b>Balance of Trades (exports - imports) Over Years<b>', title_x=0.5,
        xaxis_title='<b>Years<b>', yaxis_title='<b>Balance of Trades (usd)<b>',
        font=dict(size=12, family='Arial', color='black'), hoverlabel=dict(
            font_size=16, font_family="Rockwell", #font_color='black', bgcolor='white'
        ), plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            dtick=dtick_value,
            tickwidth=2, #tickcolor='#80ced6',
            ticks="outside",
            tickson="labels",
            rangeslider_visible=False
        ), margin=dict(l=0, r=0, t=30, b=0),

       # yaxis=dict()
    )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=True, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True, zeroline=True, linecolor='black')
    return fig


def get_top10_chart(df, selected_flow):
    fig=go.Figure()
    # filtering by flow
    df = df[df['flow'] == selected_flow]
    # grouping by country
    graph_df=df.groupby('country_or_area',sort=False)['commodity'].count()
    # getting top 10 countries
    graph_df = graph_df.nlargest(10)

    # creating the chart
    fig.add_trace(go.Bar(name=selected_flow, x=graph_df.index, y=graph_df.astype('int64'),
                         marker_color='#0096eb',orientation='v',text=graph_df.astype('int64'),
           textposition='auto'))


    fig.update_layout(title='<b>Top 10 Countries with Number of {}s<b>'.format(selected_flow),title_x=0.5,
            xaxis_title='<b>Country<b>', yaxis_title=None,
            font=dict(size=12, family='Arial', color='black'), hoverlabel=dict(
                font_size=16, font_family="Rockwell"), plot_bgcolor='white',
            paper_bgcolor='white', barmode='stack', margin=dict(l=0, r=0, t=40, b=0)
        )
    fig.update_xaxes(showgrid=False, showline=True, zeroline=False, linecolor='black', visible=True)
    fig.update_yaxes(showgrid=False, showline=True, zeroline=False, linecolor='black',
                         visible=True, showticklabels=True)

    fig.update_traces(texttemplate = '<b>%{text}</b>')

    return fig

def get_trade_balance_table(df):
    # similar to the way we got the data for balaance of trade figure but this time for every country
    df = df.groupby(['country_or_area', 'year', 'flow'])['trade_usd'].sum()
    df = df.reset_index()

    countries = []
    years_ = []
    trades_balance = []
    for country in df['country_or_area'].unique().tolist():
        filtered_country_df = df[df['country_or_area'] == country]
        years = filtered_country_df['year'].unique().tolist()

        for year in years:
            filtered_year_df = filtered_country_df[filtered_country_df['year'] == year]

            exports_df = filtered_year_df[filtered_year_df['flow'] == 'Export']
            if exports_df.empty:
                exports = 0
            else:
                exports = exports_df['trade_usd'].values[0]

            imports_df = filtered_year_df[filtered_year_df['flow'] == 'Import']
            if imports_df.empty:
                imports = 0
            else:
                imports = imports_df['trade_usd'].values[0]

            re_exports_df = filtered_year_df[filtered_year_df['flow'] == 'Re-Export']
            if re_exports_df.empty:
                re_exports = 0
            else:
                re_exports = re_exports_df['trade_usd'].values[0]

            re_imports_df = filtered_year_df[filtered_year_df['flow'] == 'Re-Import']
            if re_imports_df.empty:
                re_imports = 0
            else:
                re_imports = re_imports_df['trade_usd'].values[0]

            trade_balance = (exports + re_exports) - (imports + re_imports)
            trades_balance.append(round(trade_balance, 2))
            years_.append(year)
            countries.append(country)

    new_df = pd.DataFrame()
    new_df['Country or Area'] = countries
    new_df['Year'] = years_
    new_df['Balance of Trade (usd)'] = trades_balance

    # creating the table that contains the new_df ( balance of trade df data )
    trade_balance_table = dash_table.DataTable(
        id='trade_balance_table',
        columns=[
            {"name": i, "id": i} for i in new_df.columns
        ],
        data=new_df.to_dict("records"), filter_action='native',
        editable=False, page_size=6,
        row_deletable=False,
        style_cell=dict(textAlign='center', border='1px solid black'
                        , backgroundColor='white', color='black', fontSize=14, fontWeight=''),
        style_header=dict(backgroundColor='#0f70e0', color='white',
                          fontWeight='bold', border='1px solid black', fontSize=14),
        style_table={'overflowX': 'auto', 'width': '100%', 'min-width': '100%', 'border': '1px solid black'}
    )

    return trade_balance_table


# this function return the map figure
def get_map_figure(df):
    df_country = df.groupby(['country_or_area'])['commodity'].count()
    df_country = df_country.reset_index()
    df_country.rename(columns={'country_or_area': 'Country/Area', 'commodity': 'Number of Trades'}, inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locations=df_country['Country/Area'],
        locationmode='country names',
        colorscale="Viridis",
        z=df_country['Number of Trades'],
        colorbar=dict(title='Number of Trades')
    ))

    # im adjusting the map margins here
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), coloraxis_colorbar_x=0.9, autosize=True,
                      title='<b>Countries Overall Number of Trades<b>', title_x=0.5, font=dict(color='black', size=12))

    # this part is responsible for making the map fit to its locations
    fig.update_geos(fitbounds="locations", visible=True,  # projection=dict(type='boggs')
                    )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig
