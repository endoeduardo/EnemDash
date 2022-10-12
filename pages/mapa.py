import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import json 
import plotly.express as px

geojson = json.load(open(r'C:\Users\Eduardo Endo\Desktop\Dashboards\Assets\brasil_estados.json'))
df = pd.read_csv(r'C:\Users\Eduardo Endo\Desktop\Dashboards\MicrodadosEnem\microdadosEnem.csv')

dash.register_page(__name__)

layout = html.Div([
    dbc.Row([
        dbc.Col(
            [
                html.H3('Escolha um tipo de ensino:'),
                dcc.Dropdown(
                    id='escola-slct',
                    options=[
                        {'label':'Pública','value':'Pública'},
                        {'label':'Privada','value':'Privada'},
                        {'label':'Não Respondeu','value':'Não Respondeu'}
                    ],
                    value='Privada',
                    multi=False
                )
            ],
            style={'display':'inline-block'},
            md=6
        ),
        dbc.Col(
            [
                html.H3("Escolha a matéria:"),
                dcc.Dropdown(
                    id='materia_slct',
                    options=[
                        {'label':'Ciências da Natureza','value':'NU_NOTA_CN'},
                        {'label':'Ciências Humanas','value':'NU_NOTA_CH'},
                        {'label':'Linguagens e Códigos','value':'NU_NOTA_LC'},
                        {'label':'Matemática','value':'NU_NOTA_MT'},
                        {'label':'Redação','value':'NU_NOTA_REDACAO'}
                    ],
                    multi=False,
                    value='NU_NOTA_CN'
                )
            ],
            md=6
        )
    ]),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader([
                                html.Span('Ranking dos Estados',
                                style={'vertical-align':'center', 'justify':'center', 'padding':'2px 2px'}
                                ),
                            ]),
                            
                            dbc.CardBody(
                                id='tabela',
                                style={'padding-top':'5px', 'padding-bottom':'5px'}
                            )
                        ],
                        color='light',
                        inverse=False,
                        style={'margin':'5px 5px','height':'550px'}
                    ),
                ],
                md=3
            ),
            dbc.Col(
                [
                    dcc.Loading(
                        children=[dcc.Graph(id='mapa-fig', figure={}, style={'height':'100vh'})],
                        type='circle',
                        id='Loading-3'
                    )
                ],
                md=9,
            )
        ]
    )
])

@callback(
    [
        Output('mapa-fig', 'figure'),
        Output('tabela', 'children')
    ],    
    [
        Input('escola-slct', 'value'),
        Input('materia_slct', 'value')
    ]
)
def update(escola, materia):
    dff = df.copy()
    mask = dff[dff['TP_ESCOLA'].isin([escola])]
    notas = mask[['SG_UF_PROVA', materia]].groupby(['SG_UF_PROVA']).mean().reset_index()

    #Cria o gráfico
    fig = px.choropleth_mapbox(notas, geojson=geojson, locations='SG_UF_PROVA', color=materia,
                        color_continuous_scale='Blues',
                        mapbox_style='carto-positron',
                        center={'lat':-15.967172, 'lon':-49.687907},
                        zoom=3
            )
    fig.update_layout(
        coloraxis_showscale=False
    )
    
    #Criando um ranking
    ranking = notas.copy()
    ranking['ranking'] = ranking[materia].rank(ascending=False)
    #Ordenando o ranking
    ranking.sort_values(by=materia, ascending=False, inplace=True)
    #Arredonda o valor das notas
    ranking[materia] = ranking[materia].round(decimals=1)

    #Criando uma tabela
    tabela = dash_table.DataTable(
        columns=[{'name':i, 'id':i} for i in ranking.columns], #Criando e passando um id para as colunas
        data=ranking.to_dict('records'),
        fixed_rows={'headers': True}, # fixando o cabeçalho para que a barra de rolamento não esconda o cabeçalho
        style_table={'height': '70vh', 'overflowY': 'auto'}, # adicionando uma barra de rolamento, e fixando o tamanho da tabela em 400px
        style_header={'textAlign': 'center', 'padding':'2px 2px'}, # centralizando o texto do cabeçalho
        style_cell={'textAlign': 'center', 'font-size': '14px'}, # centralizando o texto das céluas e alterando o tamanho da fonte
        style_as_list_view=True, # deixa a tabela sem bordas entre as colunas
        style_data_conditional=[ # este parametro altera a cor da célula quando o usuário clica na célula
            {
                "if": {"state": "selected"},
                "backgroundColor": "rgba(205, 205, 205, 0.3)",
                "border": "inherit !important",
            }
        ],                      
    )

    return fig, [tabela]