import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

df = pd.read_csv(r"C:\Users\Eduardo Endo\Desktop\Dashboards\MicrodadosEnem\microdadosEnem.csv")

dash.register_page(__name__)
layout = html.Div([
    dbc.Row(
        [
            html.H4("Escolha a matéria:"),
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
        style={'display':'inline-block'}
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Média da Nota", style={'text-align':'center'}),
                                        html.H5(id="media-nota-text", style={'text-align':'center'})
                                    ]
                                )
                            ],
                            color='primary',
                            inverse=True,
                            style={'margin':'25px 25px'}
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("Nota Máxima", style={'text-align':'center'}),
                                        html.H5(id="nota-maxima-text", style={'text-align':'center'})
                                    ]
                                )
                            ],
                            color='primary',
                            inverse=True,
                            style={'margin':'25px 25px'}
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(id="qte-pessoas-text", style={'text-align':'center'}),
                                        # html.H4("Tiraram a nota máxima")
                                    ]
                                )
                            ],
                            color='primary',
                            inverse=True,
                            style={'margin':'25px 25px'}
                        ),
                    ]),
                ],
                md=3
            ),
            dbc.Col(
                [
                    dcc.Loading(
                        id='loading-1', type='circle',
                        children=[
                            dcc.Graph(id='histograma-notas', figure={})
                        ]
                        )
                ],
                md=9
            )
        ]
    ),
    dbc.Row(
        [
            dcc.Loading(
                id='loading-2', type='circle',
                children=[
                    dcc.Graph(id='violin-graph', figure={})
                ]
            )
        ]
    )
])


@callback(
    [
        Output('histograma-notas', 'figure'),
        Output('media-nota-text', 'children'),
        Output('nota-maxima-text', 'children'),
        Output('qte-pessoas-text', 'children'),
        Output('violin-graph', 'figure')
    ],
    [Input('materia_slct', 'value')]
)
def update(materia):
    dff = df.copy()
    dff.dropna(inplace=True)

    #Criando o plot
    fig = px.histogram(dff, x=str(materia), color='TP_SEXO', labels={'TP_SEXO':"Gênero"})

    #Contando a média de nota
    media = dff[materia].mean()
    media_txt = f"{media:.2f}"

    #Calculando a nota máxima
    maxima = dff[materia].max()
    maxima_txt = f"{maxima}"

    #Quantas pessoas tiraram a nota máxima
    qte_pessoas = len(dff[dff[materia] == maxima])
    qte_txt = f"{qte_pessoas} pessoa(s) tiraram a nota máxima"

    #Plot violino
    fig2 = px.violin(
        dff, x='TP_ESCOLA', y=materia, color='TP_SEXO', 
        labels={'TP_ESCOLA':'Tipo de Ensino', 'TP_SEXO':'Gênero'})

    return fig, media_txt, maxima_txt, qte_txt, fig2