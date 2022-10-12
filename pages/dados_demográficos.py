import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv(r"C:\Users\Eduardo Endo\Desktop\Dashboards\MicrodadosEnem\microdadosEnem.csv")

dash.register_page(__name__, path='/')
layout = html.Div([
            dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4('Selecione a raça:'),
                            ],
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id='race_slct',
                                    options=[{'label':str(x), 'value':x} for x in df["TP_COR_RACA"].unique().tolist()],
                                    multi=True,
                                    value=["Branca", "Amarela", "Preta", "Parda", "Não Declarado", "Indígena"]
                                )
                            ]
                        )
                    ],
                    style={'display':'inline-block'}
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                
                                html.Div(dcc.Graph(id='distribuicao-etaria', figure={}))
                                
                                
                            ],
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H4("Tipo de Ensino"),
                                                html.P(id="escola-ratio-text")
                                            ]
                                        )
                                    ],
                                    color='primary',
                                    inverse=True
                                ),
                                html.Div(dcc.Graph(id='escola-bar', figure={}))
                            ],
                            md=6
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H4("Razão de Gênero"),
                                                html.P(id="genero-ratio-text")
                                            ]
                                        )
                                    ],
                                    color='primary',
                                    inverse=True
                                ),
                                html.Div(dcc.Graph(id='genero-bar', figure={}))
                            ],
                            md=6
                        )
                    ],
                    # style={'display':'inline-block'}
                )
])


@callback(
    [
        Output(component_id='distribuicao-etaria', component_property='figure'),
        Output(component_id='genero-bar', component_property='figure'),
        Output(component_id='escola-bar', component_property='figure'),
        Output(component_id='escola-ratio-text', component_property='children'),
        Output(component_id='genero-ratio-text', component_property='children')
    ],
    [Input(component_id='race_slct', component_property='value')]
)
def update_dist_etaria(race_slct):
    #Segmentado o dataframe
    dff = df.copy()
    mask = dff[dff["TP_COR_RACA"].isin(race_slct)]
    fx = mask["TP_FAIXA_ETARIA"].value_counts()

    #Criando o gráfico de distribuição etária
    fig1 = px.bar(fx, x=fx.keys(), y=fx.values, 
    # title="Distribuição de Faixa Etária", 
    labels={'y':'Contagem', 'index':'Faixa Etária'})

    #Criando o gráfico de barra de gênero
    sexo = mask['TP_SEXO'].value_counts()   
    fig2 = px.bar(sexo, x=sexo.keys(), y=sexo.values, color=sexo.keys(),
        # title="Quantidade de gênero", 
        labels={'y':'Contagem', 'index':'Gênero'},
        color_discrete_sequence=['red', 'blue'])
    genero_ratio = sexo["F"]/sexo["M"]
    genero_ratio_text = f"A razão de Mulheres/Homens é de {genero_ratio:.2f}"

    #Criando o gráfico de barra para escolas
    tpescola = mask['TP_ESCOLA'].value_counts()
    fig3 = px.bar(tpescola, x=tpescola.keys(), y=tpescola.values, color=tpescola.keys(),
            labels={'y':'Contagem', 'index':'Tipo de Ensino'})
    escola_ratio = tpescola["Pública"]/tpescola["Privada"]
    escola_ratio_text = f"Para cada aluno no ensino privado existem {escola_ratio:.2f} no ensino público"
    return fig1, fig2, fig3, escola_ratio_text, genero_ratio_text
