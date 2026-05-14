import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# 1. Carga de datos
df = pd.read_csv('Encuesta sobre Videojuegos en Steam.csv')
columna_waffle = 'Si un juego tiene MUCHOS jugadores activos pero malas reseñas, ¿lo jugarías/comprarías igual?  '

# 2. Procesamiento de frecuencias
counts = df[columna_waffle].value_counts()
total = sum(counts)

# 3. Configuración de la cuadrícula (Waffle)
width = 10
height = 5
total_tiles = width * height

# Calcular cuántos cuadros corresponden a cada categoría
tiles_per_cat = {k: int(round((v / total) * total_tiles)) for k, v in counts.items()}

# Ajuste manual para asegurar que sumen exactamente el total de cuadros (50)
diff = total_tiles - sum(tiles_per_cat.values())
if diff != 0:
    cat_max = max(tiles_per_cat, key=tiles_per_cat.get)
    tiles_per_cat[cat_max] += diff

# 4. Construcción de la matriz del gráfico
waffle = np.zeros((height, width))
cat_list = list(counts.keys())

curr_tile = 0
for i, cat in enumerate(cat_list):
    for _ in range(tiles_per_cat[cat]):
        row = curr_tile // width
        col = curr_tile % width
        waffle[row, col] = i + 1
        curr_tile += 1

# 5. Visualización
plt.figure(figsize=(10, 6))
plt.pcolor(waffle[::-1], cmap='tab10', edgecolors='white', linewidths=2)

# Crear la leyenda personalizada
legend_elements = [
    Patch(facecolor=plt.cm.tab10(i/10), label=f"{cat} ({counts[cat]})") 
    for i, cat in enumerate(cat_list)
]

plt.legend(
    handles=legend_elements, 
    loc='lower center', 
    bbox_to_anchor=(0.5, -0.25), 
    ncol=2, 
    frameon=False
)

plt.title('¿Jugarías un juego popular con malas reseñas?', fontsize=14, pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()