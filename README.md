# Repositorio_Tareas_Grupo_Videojuegos
Integrantes: 
 - Ignacio Salas 202173142-3
 - Benjamin Vilches 202173101-6
 - Claudio Villagrán 202021016-0

Para correr los codigos se deben ejecutar las siguientes librerias:
 - pip install plotly kaleido matplotlib pandas seaborn

 Luego para la obtencion de steam_top.json:
 1. Se recoletaron los 100 juegos más jugados en steam según steamDB
 2. Se recolecto manualmente de cada juego el appid, que se obtiene al buscar el juego en la tienda de steam (aparece en el link)
 3. Con el appid se recolectaron los datos con el archivo steam_pipeline.py y luego steam_pipeline_anio.py directamente de la API de steam
 4. Finalmente se agrego la nota de los juegos que no tenian su nota en steam manualmente desde el sitio de metacritic