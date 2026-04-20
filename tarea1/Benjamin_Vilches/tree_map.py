import pandas as pd
import plotly.express as px
import json


with open('steam_top.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)

df['jugadores_activos'] = pd.to_numeric(df['jugadores_activos'])
df['genero_principal'] = df['generos'].apply(lambda x: x.split(',')[0].strip() if x else 'Otros')

df['nota_metacritic'] = df['nota_metacritic'].fillna(df['nota_metacritic'].mean())

fig = px.treemap(
    df, 
    path=[px.Constant("Mercado Steam"), 'genero_principal', 'nombre'], 
    values='jugadores_activos',
    color='nota_metacritic',
    color_continuous_scale='Viridis', 
    title='Top de juegos de Steam por jugadores activos y nota Metacritic'
)

fig.update_traces(
    marker=dict(colorbar=dict(title=dict(text='Nota Metacritic'))),
    textinfo="label+value",
    texttemplate="<b>%{label}</b><br>%{value:,.0f} jugadores",
    hovertemplate='<b>%{label}</b><br>Jugadores: %{value:,.0f}<br>Metacritic: %{color:.1f}'
)

fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))


fig.show()
fig.write_image("treemap_steam.png")