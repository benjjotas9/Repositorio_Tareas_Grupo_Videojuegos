import pandas as pd
import plotly.graph_objects as go
import json

# 1. Cargar datos
with open('steam_top.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# 2. Preprocesamiento alineado al Hilo Conductor
# Extraemos el género principal y limpiamos para evitar bucles con 'Indie'
df['genero_principal'] = df['generos'].apply(lambda x: x.split(',')[0].strip() if x else 'Otros')

def filtrar_destino(row):
    if row['genero_principal'] == 'Indie':
        parts = row['generos'].split(',')
        return parts[1].strip() if len(parts) > 1 else 'Otros'
    return row['genero_principal']

df['genero_principal'] = df.apply(filtrar_destino, axis=1)

# Filtro de géneros solicitado
excluir = ['Deportes', 'Multijugador masivo']
df_final = df[~df['genero_principal'].isin(excluir)].copy()

# Agrupamos por la suma de JUGADORES ACTIVOS (Medida del éxito)
flujos = df_final.groupby(['categoria', 'genero_principal'])['jugadores_activos'].sum().reset_index(name='total_players')

# 3. Mapeo de índices para Plotly
all_nodes = list(pd.unique(flujos[['categoria', 'genero_principal']].values.ravel('K')))
node_indices = {name: i for i, name in enumerate(all_nodes)}

source = flujos['categoria'].map(node_indices).tolist()
target = flujos['genero_principal'].map(node_indices).tolist()
value = flujos['total_players'].tolist()

# 4. Configuración Visual (Estética Dark Steam)
node_colors = ['#66c0f4' if n in df_final['categoria'].unique() else '#2a475e' for n in all_nodes]
link_colors = ['rgba(102, 192, 244, 0.4)' for _ in range(len(source))]

# 5. Generación del Gráfico
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20,
        line=dict(color="white", width=0.5),
        label=all_nodes, color=node_colors
    ),
    link=dict(source=source, target=target, value=value, color=link_colors)
)])

fig.update_layout(
    title_text="Flujo de Éxito: Distribución de Audiencia por Tipo de Estudio y Género",
    template='plotly_dark',
    paper_bgcolor='#1b2838',
    font_size=12
)

fig.show()
fig.write_image("sankey.png")