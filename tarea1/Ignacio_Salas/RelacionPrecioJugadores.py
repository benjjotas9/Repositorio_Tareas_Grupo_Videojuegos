import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#Cargamos los datos

with open("steam_top.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

#Eliminamos deadlock, ya que aun no sale oficialmente
#Pasamos el precio como int

df = df[df["nombre"] != "Deadlock"]

def limpiar_precio(p):
    if p == "Free/N/A":
        return 0
    p = p.replace("CLP$", "").replace(".", "").strip()
    try:
        return int(p)
    except:
        return None

df["precio"] = df["precio_actual"].apply(limpiar_precio)

df["anio_lanzamiento"] = pd.to_numeric(df["anio_lanzamiento"], errors="coerce")

df = df.dropna(subset=["precio", "jugadores_activos", "anio_lanzamiento"])

df["anio_lanzamiento"] = df["anio_lanzamiento"].astype(int)


#Rangos de año de los juegos

df["grupo_anio"] = pd.cut(
    df["anio_lanzamiento"],
    bins=[2000, 2010, 2015, 2020, 2023, 2026],
    labels=["2000-10", "2010-15", "2015-20", "2020-23", "2023-26"]
)

df = df.dropna(subset=["grupo_anio"])

#Gráfico

plt.figure(figsize=(12, 8))

scatter = sns.scatterplot(
    data=df,
    x="precio",
    y="jugadores_activos",
    hue="grupo_anio",                
    size="jugadores_activos",    
    sizes=(30, 300),
    palette="tab10",
    alpha=0.7,
    edgecolor="black"
)


# Escala log 
plt.yscale("log")


#Titulo y labels

plt.title("Precio vs Popularidad")
plt.xlabel("Precio (CLP)")
plt.ylabel("Jugadores activos en escala logarítmica")

#Leyenda


handles, labels = scatter.get_legend_handles_labels()

# Separar partes
n_grupos = len(df["grupo_anio"].unique())

# Primera parte contiene rangos de año
handles_color = handles[1:n_grupos+1]
labels_color = labels[1:n_grupos+1]

# Segunda parte los tamaños
handles_size = handles[n_grupos+2:]
labels_size = labels[n_grupos+2:]


# Leyenda de colores
legend1 = plt.legend(
    handles_color,
    labels_color,
    title="Rango de año",
    loc="upper left",
    bbox_to_anchor=(1.02, 1)
)

# Leyenda de tamaños 
legend2 = plt.legend(
    handles_size,
    labels_size,
    title="Jugadores",
    loc="upper left",
    bbox_to_anchor=(1.02, 0.55),
    labelspacing=1.5            
)

plt.gca().add_artist(legend1)


plt.tight_layout()
plt.show()