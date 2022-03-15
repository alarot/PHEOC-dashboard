import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import glob

# Opening the data files with pandas
data_files = glob.glob('./Data/*.csv')
df_list = []
for file in data_files:
    data = pd.read_csv(file)
    df_list.append(data)
df = pd.concat(df_list)
df['DATE'] = pd.to_datetime(df['DATE'], format="%d/%m/%Y")
df['MONTH'] = df['DATE'].dt.month
date_label = df['MONTH'].unique()
date_label.sort()
months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]
df['INDICATOR'] = df['INDICATOR'].apply(lambda x: x.title())
label = df['INDICATOR'].unique()
# List of counties
main_counties = list(df.COUNTY.unique())
counties = list(df.COUNTY.unique())
counties.insert(0, 'All')


# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.title = 'PHEOC Dashboard'
app.description = "Public Health Emergency Operation Centre Support Supervision Checklist"
app.layout = html.Div(
    children=[
        html.Div([
            # Adds heading   DIV
            html.Div([
                # Header
                html.Div([
                    html.H3(
                        'Public Health Emergency Operations Checklist',
                        style={
                            'margin-bottom': '0px',
                            'color': '#F0A500',
                            'font-family': "'Open Sans', sans-serif",
                            'font-weight': 600,
                            'font-size': '3rem',
                            'letter-spacing': '0.12rem'
                        }
                    )
                ])
            ], id='title', className='one-third column',
                style={'text-align': 'center', 'margin': '0 auto', 'font-size': '1.5rem'}),
        ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

        # 1 ROW, 2 COLS
        html.Div([
            # Indicator Scores By Month & County
            html.Div([
                html.Label(
                    'Indicator Scores By Month & County',
                    style={
                        'color': '#E6D5B8',
                        'font-weight': 400,
                        'font-size': '2rem',
                        'font-family': "'Open Sans', sans-serif",
                        'text-align': 'center'
                    }
                ),
                html.Div([
                    html.Div([
                        html.Label('Indicator',
                                   style={'color': '#E6D5B8',
                                          'font-weight': 400,
                                          'font-size': '1.5rem',
                                          'font-family': "'Open Sans', sans-serif",
                                          }),
                        dcc.Dropdown(
                            id='indicators',
                            options=[
                                {'label': i.title(), 'value': i} for i in label
                            ],
                            placeholder='Select Indicator'
                        ),
                    ], className='card_container five columns'),
                    # END DROPDOWN
                    # START COUNTY DROPDOWN
                    html.Div([
                        html.Label(
                                'Month',
                                style={
                                    'color': '#E6D5B8',
                                    'font-weight': 400,
                                    'font-size': '1.5rem',
                                    'font-family': "'Open Sans', sans-serif"
                                }
                        ),
                        dcc.Dropdown(
                            id='month',
                            options=[
                                {'label': months[i-1], 'value': i} for i in date_label
                            ],
                            placeholder='Select Month'
                        ),
                    ], className='card_container five columns'),
                    # END COUNTY DROPDOWN
                ], className='row flex display'),
                dcc.Graph(id='bar'),
                ], className='card_container six columns'),
            # AGGREGATES GRAPH
            html.Div([
                html.Label(
                    'Cumulative Indicator Scores by County',
                    style={
                        'color': '#E6D5B8',
                        'font-weight': 400,
                        'font-size': '2rem',
                        'font-family': "'Open Sans', sans-serif",
                        'text-align': 'center'
                    }
                ),
                # START INDICATOR DROPDOWN
                html.Div([
                    html.Div([
                        html.Label('Indicator',
                                   style={'color': '#E6D5B8',
                                          'font-weight': 400,
                                          'font-size': '1.5rem',
                                          'font-family': "'Open Sans', sans-serif",
                                          }),
                        dcc.Dropdown(
                            id='indicator',
                            options=[
                                {'label': i.title(), 'value': i} for i in label
                            ],
                            placeholder='Select Indicator'
                        ),
                    ], className='card_container five columns'),
                    # END DROPDOWN
                    # START COUNTY DROPDOWN
                    html.Div([
                        html.Label(
                                'County',
                                style={
                                    'color': '#E6D5B8',
                                    'font-weight': 400,
                                    'font-size': '1.5rem',
                                    'font-family': "'Open Sans', sans-serif"
                                }
                        ),
                        dcc.Dropdown(
                            id='county',
                            options=[
                                {'label': i, 'value': i} for i in counties
                            ],
                            value='All'
                        ),
                    ], className='card_container five columns'),
                    # END COUNTY DROPDOWN
                ], className='row flex display'),
                dcc.Graph(id='graph'),
                ], className='card_container six columns'),
        ], className='row flex-display'),
        html.Div([
            html.Label(
                'All Indicators per County',
                style={
                    'color': '#E6D5B8',
                    'font-weight': 400,
                    'font-size': '2rem',
                    'font-family': "'Open Sans', sans-serif",
                    'text-align': 'center',
                    'margin-bottom': '32px'
                }
            ),
            html.Div([
                # START COUNTY DROPDOWN
                html.Div([
                    html.Label(
                        'County',
                        style={
                            'color': '#E6D5B8',
                            'font-weight': 400,
                            'font-size': '1.5rem',
                            'font-family': "'Open Sans', sans-serif"
                        }
                    ),
                    dcc.Dropdown(
                        id='county_2',
                        options=[
                            {'label': i, 'value': i} for i in main_counties
                        ],
                        placeholder='Select County'
                    ),
                ], className='card_container four columns', style={'margin-bottom': '32px'}),
                # END COUNTY DROPDOWN
            ], className='row flex display'),
            dcc.Graph(id='graph_2'),
        ], className='card_container twelve columns')
    ], id='mainContainer'
)


# Compare Individual Counties for individual Months
@app.callback(
    Output(component_id='bar', component_property='figure'),
    [
        Input(component_id='indicators', component_property='value'),
        Input(component_id='month', component_property='value')
    ]
)
def render_bars(indicators, month):
    data = df[(df.MONTH == month) & (df.INDICATOR == indicators)]
    trace = go.Bar(
        x=data['COUNTY'],
        y=data['SCORE'],
        marker = dict(color='#E45826')
    )
    fig_2 = go.Figure(data=trace)
    fig_2.update_layout(
        title=dict(text=indicators, font_color='#F0A500', font_size=30, x=0.5, font_family="Arial"),
        xaxis=dict(title='County', color='#F0A500', title_font_size=20, title_font_family="Arial"),
        yaxis=dict(title='% Score', color='#F0A500', showgrid=True, gridwidth=0.1,
                   gridcolor='#313030', title_font_size=20, title_font_family="Arial"),
        hoverlabel=dict(bgcolor='#F0A500'),
        autosize=True,
        paper_bgcolor='#1B1A17',
        plot_bgcolor='#1B1A17',
    )
    return fig_2


# Visualize All the Aggregates
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [
        Input(component_id='indicator', component_property='value'),
        Input(component_id='county', component_property='value')
     ]
)
def render_graph(indicator, county):
    data = df[df['INDICATOR'] == indicator]
    if county == "All":
        data = data.groupby('DATE').SCORE.sum().reset_index()
        data.sort_values(by='DATE')
    else:
        data = data[data.COUNTY == county].sort_values(by='DATE').reset_index()
    # Graph with plotly GO
    trace1 = go.Scatter(
        x=data['DATE'],
        y=data['SCORE'],
        mode='lines',
        line=dict(color='#F0A500', width=0.5),
        marker=dict(color='#F0A500', size=4)
    )

    fig = go.Figure(data=trace1)
    fig.update_layout(
        title=dict(text=indicator, font_color='#F0A500', font_size=30, x=0.5, font_family="Arial"),
        xaxis=dict(title='Date', color='#F0A500', showgrid=False, showspikes=True,
                   spikethickness=1, spikedash='solid', spikemode='toaxis+across+marker',
                   spikecolor='#E45826', spikesnap='cursor', title_font_size=20, title_font_family="Arial"),
        yaxis=dict(title='% Score', color='#F0A500', showgrid=True, gridwidth=0.1,
                   gridcolor='#313030', title_font_size=20, title_font_family="Arial"),
        hoverlabel=dict(bgcolor='#F0A500'),
        hovermode='x',
        autosize=True,
        paper_bgcolor='#1B1A17',
        plot_bgcolor='#1B1A17',
    )
    return fig


# Visualize the bottom bar chart
@app.callback(
    Output(component_id='graph_2', component_property='figure'),
    Input(component_id='county_2', component_property='value')
)
def render_bottom_bars(county):
    data = df[df.COUNTY == county]

    trace = px.bar(
        data,
        x='INDICATOR',
        y='SCORE',
        color="FOLLOW_UP",
        barmode="group",
        color_discrete_sequence=['#F0A500', '#00B4D8', '#E45826', '#FA4EAB']
    )
    fig_2 = go.Figure(data=trace)
    fig_2.update_layout(
        title=dict(text=county, font_color='#F0A500', font_size=30, x=0.5, font_family="Arial"),
        xaxis=dict(title='Indicators', color='#F0A500', title_font_size=20, title_font_family="Arial"),
        yaxis=dict(title='% Score', color='#F0A500', showgrid=True, gridwidth=0.1,
                   gridcolor='#313030', title_font_size=20, title_font_family="Arial"),
        legend=dict(yanchor="bottom", y=0, xanchor="right", x=1.1, bgcolor="black",
                    font=dict(size=12, color="#E6D5B8"), title=dict(text='Follow Up'), bordercolor="#E6D5B8",
                    borderwidth=0.1),
        hoverlabel=dict(bgcolor='#F0A500'),
        hovermode='x',
        autosize=True,
        paper_bgcolor='#1B1A17',
        plot_bgcolor='#1B1A17',
    )

    return fig_2

if __name__ == "__main__":
    app.run_server(debug=True)
