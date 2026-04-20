import pandas as pd
import plotly.express as px
import json
from pathlib import Path

# Cargar datos
base_dir = Path(__file__).resolve().parent
json_path = base_dir / "steam_top.json"
output_path = base_dir / "sunburst.png"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)
df = df.dropna(subset=['categoria'])

# Mapeo de User Score (0-100)
rev_map = {"Overwhelmingly Positive": 96, "Very Positive": 88, "Mostly Positive": 75, "Positive": 65, "Mixed": 50, "Mostly Negative": 30}
df['user_score_num'] = df['porcentaje_reseñas_positivas'].map(rev_map)
df = df.dropna(subset=['user_score_num'])

# Generar gráfico sunburst
fig = px.sunburst(df, 
                  path=['categoria', 'nombre'], # Jerarquía: Primero categoría, luego juego
                  values='jugadores_activos',    # El tamaño depende de los jugadores
                  color='user_score_num',       # El color depende de la nota de usuarios
                  color_continuous_scale='RdYlGn', # Rojo (mal) a Verde (bien)
                  range_color=[50, 100],
                  title="<b>Tamaño del mercado de Steam por categoría de estudio</b><br><sup>Tamaño del segmento = jugadores activos | Color = valoración de usuarios</sup>")

# Ajustar barra de color para que el título y la posición sean claros
fig.update_layout(
    title_x=0.5,
    title_xanchor="center",
    margin=dict(r=220, t=95),
    coloraxis_colorbar=dict(
        title=dict(text=""),
        x=1.03,
        y=0.5,
        yanchor="middle",
        len=0.8,
        xanchor="center"
    ),
    annotations=[
        dict(
            text="Valoración de usuario",
            x=1.03,
            y=0.93,
            xref="paper",
            yref="paper",
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=18, color="#2a3f5f")
        )
    ]
)

# Hover interactivo: mostrar nombre, valoración y jugadores de forma clara
fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Valoración de usuario: %{color:.0f}/100<br>"
        "Jugadores activos: %{value:,}<extra></extra>"
    )
)

# Abrir gráfico interactivo directamente al ejecutar el script
fig.show(config={
    "scrollZoom": True,
    "displaylogo": False
})

# Guardar también imagen estática 
fig.write_image(str(output_path))