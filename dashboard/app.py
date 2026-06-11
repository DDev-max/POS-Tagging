import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud

df_pos = pd.read_csv("data/results/pos_tagging_df.csv", sep=';')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Análisis de Texto y POS por Lugar"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Análisis Morfosintáctico de Reseñas Turísticas", 
                        className="text-center text-primary my-4 font-weight-bold"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.Row([
                    dbc.Col(
                        html.Img(
                            id='imagen-lugar', 
                            style={
                                'width': '100%', 
                                'height': '200px', 
                                'objectFit': 'cover', 
                                'borderRadius': '5px 0 0 5px'
                            }
                        ), 
                        lg=4, md=5, xs=12
                    ),
                    dbc.Col(
                        html.Div([
                            html.H2(id='titulo-lugar', className="text-primary font-weight-bold mb-1"),
                        ], className="d-flex flex-column justify-content-center h-100 p-4"),
                        lg=8, md=7, xs=12
                    )
                ], className="g-0 align-items-center")
            ], className="shadow-sm mb-4 overflow-hidden")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Selecciona un Lugar para Filtrar el Reporte:", className="font-weight-bold mb-2"),
                    dcc.Dropdown(
                        id='dropdown-lugar',
                        options=[{'label': lugar, 'value': lugar} for lugar in df_pos['lugar'].unique()],
                        value=df_pos['lugar'].unique()[0], 
                        clearable=False,
                        className="text-dark"
                    )
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Distribución Porcentual y Total del POS", className="bg-primary text-white font-weight-bold"),
                dbc.CardBody([
                    dcc.Graph(id='grafico-pos'),
                    html.Hr(),
                    html.P(id='texto-explicativo-pos', className="text-justify text-secondary mt-2 small")
                ])
            ], className="shadow-sm mb-4")
        ], lg=7, md=12),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 3 Elementos NER más Frecuentes", className="bg-primary text-white font-weight-bold"),
                dbc.CardBody([
                    dcc.Graph(id='grafico-ner'),
                    html.Hr(),
                    html.P(id='texto-explicativo-ner', className="text-justify text-secondary mt-2 small")
                ])
            ], className="shadow-sm mb-4")
        ], lg=5, md=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sustantivos, Adjetivos y Verbos más comunes", className="bg-info text-white font-weight-bold"),
                dbc.CardBody([
                    dcc.Graph(id='nubes-categorias'),
                    html.Hr(),
                    html.P(id='texto-explicativo-cat', className="text-justify text-secondary mt-2")
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Análisis de Sentimiento: Palabras en Reseñas Positivas vs Negativas", className="bg-success text-white font-weight-bold"),
                dbc.CardBody([
                    dcc.Graph(id='nubes-sentimientos'),
                    html.Hr(),
                    html.P(id='texto-explicativo-sent', className="text-justify text-secondary mt-2")
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ])
    
], fluid=True)


@app.callback(
    [Output('titulo-lugar', 'children'),       
     Output('imagen-lugar', 'src'),            
     Output('grafico-pos', 'figure'),
     Output('grafico-ner', 'figure'),
     Output('nubes-categorias', 'figure'),
     Output('nubes-sentimientos', 'figure'),
     Output('texto-explicativo-pos', 'children'),
     Output('texto-explicativo-ner', 'children'),
     Output('texto-explicativo-cat', 'children'),
     Output('texto-explicativo-sent', 'children')],
    [Input('dropdown-lugar', 'value')]
)
def actualizar_reporte(lugar_seleccionado):
    ruta_imagen = f"/assets/{lugar_seleccionado}.jpg" 
    texto_titulo = f"Explorando: {lugar_seleccionado}"
    
    df_lugar = df_pos[df_pos['lugar'] == lugar_seleccionado]
    
    total = df_lugar[df_lugar['tipo'] == 'POS'].groupby('categoria')['frecuencia'].sum()
    total['NER'] = df_lugar[df_lugar['tipo'] == 'NER']['frecuencia'].sum()
    suma_lugar = total.sum()
    porcentajes = (total / suma_lugar) * 100
    
    fig_pos = go.Figure(go.Bar(
        x=porcentajes.values,
        y=porcentajes.index,
        orientation='h',
        text=total.values,
        textposition='inside',
        insidetextanchor='end',
        marker=dict(color=px.colors.qualitative.G10[:len(total)])
    ))
    fig_pos.update_layout(xaxis_title="% del Total", yaxis_title="Categoría", margin=dict(l=20, r=20, t=20, b=20), height=320)
    
    df_ner = df_lugar[df_lugar['tipo'] == 'NER'].nlargest(3, 'frecuencia')
    fig_ner = px.bar(df_ner, x='frecuencia', y='elemento', orientation='h', color_discrete_sequence=['#636EFA'])
    fig_ner.update_layout(xaxis_title="Frecuencia", yaxis_title="Elemento NER", margin=dict(l=20, r=20, t=20, b=20), height=320)
    fig_ner.update_yaxes(categoryorder="total ascending")
    
    from plotly.subplots import make_subplots
    fig_cat_subplots = make_subplots(rows=1, cols=3, subplot_titles=('Verbos', 'Adjetivos', 'Sustantivos'))
    categorias = ['VERB', 'ADJ', 'NOUN']
    colormaps = ['viridis', 'plasma', 'inferno']
    
    for i, cat in enumerate(categorias):
        df_cat = df_lugar[(df_lugar['categoria'] == cat)]
        frecuencias = dict(zip(df_cat["elemento"], df_cat["frecuencia"]))
        if frecuencias:
            wc = WordCloud(width=400, height=400, background_color="white", colormap=colormaps[i]).generate_from_frequencies(frecuencias)
            fig_cat_subplots.add_trace(go.Image(z=wc.to_array()), row=1, col=i+1)
        fig_cat_subplots.update_xaxes(visible=False, row=1, col=i+1).update_yaxes(visible=False, row=1, col=i+1)
    fig_cat_subplots.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
    
    fig_sent_subplots = make_subplots(rows=1, cols=2, subplot_titles=('Positivas', 'Negativas'))
    no_stopwords = df_lugar[df_lugar['categoria'].isin(['VERB', 'ADJ', 'NOUN'])]
    negativas = no_stopwords[(no_stopwords['rating_5'] == 0) & (no_stopwords['rating_4'] == 0)].nlargest(700, 'frecuencia')
    positivas = no_stopwords[(no_stopwords['rating_1'] == 0) & (no_stopwords['rating_2'] == 0) & (no_stopwords['rating_3'] == 0)].nlargest(700, 'frecuencia')
    
    frecuencias_neg = dict(zip(negativas["elemento"], negativas["frecuencia"]))
    frecuencias_pos = dict(zip(positivas["elemento"], positivas["frecuencia"]))
    
    if frecuencias_pos:
        wc_pos = WordCloud(width=500, height=400, background_color='white', colormap='Greens').generate_from_frequencies(frecuencias_pos)
        fig_sent_subplots.add_trace(go.Image(z=wc_pos.to_array()), row=1, col=1)
    if frecuencias_neg:
        wc_neg = WordCloud(width=500, height=400, background_color='white', colormap='Reds').generate_from_frequencies(frecuencias_neg)
        fig_sent_subplots.add_trace(go.Image(z=wc_neg.to_array()), row=1, col=2)
        
    fig_sent_subplots.update_xaxes(visible=False, row=1, col=1).update_yaxes(visible=False, row=1, col=1)
    fig_sent_subplots.update_xaxes(visible=False, row=1, col=2).update_yaxes(visible=False, row=1, col=2)
    fig_sent_subplots.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
    
    cat_max = porcentajes.idxmax() if not porcentajes.empty else "N/A"
    
    top_ner_elem = df_ner.iloc[0]['elemento'] if not df_ner.empty else "N/A"
    
    exp_pos = f"Análisis de Distribución en {lugar_seleccionado}: Se observa un predominio notable de la categoría '{cat_max}' dentro del corpus de texto analizado, lo que define el estilo y estructura comunicativa principal de las reseñas de este sitio."
    
    exp_ner = f"Identificación de Entidades: Para {lugar_seleccionado}, la entidad de mayor relevancia detectada mediante reconocimiento NER es '{top_ner_elem}'. Esto sugiere que los usuarios tienden a centralizar sus opiniones o experiencias en torno a este elemento en particular."
    
    exp_cat = f"Campos Semánticos Clave: Las nubes de palabras revelan los verbos de acción, adjetivos calificativos y sustantivos más recurrentes en {lugar_seleccionado}. Esta segmentación morfológica permite aislar los núcleos conceptuales de las opiniones sin el ruido de las palabras de parada (stopwords)."
    
    exp_sent = f"Polaridad del Discurso en {lugar_seleccionado}: La comparativa semántica muestra un claro contraste. Mientras que el espectro positivo (Verde) tiende a enfocarse en aspectos satisfactorios de la experiencia, el espectro negativo (Rojo) delimita con precisión las principales quejas o áreas de oportunidad reportadas."

    return (texto_titulo, ruta_imagen, fig_pos, fig_ner, fig_cat_subplots, fig_sent_subplots,
            exp_pos, exp_ner, exp_cat, exp_sent)

if __name__ == '__main__':
    app.run(debug=True)