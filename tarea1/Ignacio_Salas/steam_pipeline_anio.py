import requests
import json
import time

# Cargar tu dataset
with open("steam_top_completo.json", "r", encoding="utf-8") as f:
    juegos = json.load(f)

def obtener_anio(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data[str(appid)]["success"]:
            info = data[str(appid)]["data"]

            if "release_date" in info and info["release_date"]["date"]:
                fecha = info["release_date"]["date"]
                
                # Extraer el año (últimos 4 caracteres)
                anio = fecha[-4:]
                return anio

    except Exception as e:
        print(f"Error con appid {appid}: {e}")

    return None


# Añadir año a cada juego
for juego in juegos:
    appid = juego["appid"]
    print(f"Procesando {juego['nombre']} ({appid})...")
    
    anio = obtener_anio(appid)
    juego["anio_lanzamiento"] = anio

    time.sleep(1.2)  # evitar bloqueo de Steam

# Guardar nuevo archivo
with open("steam_top_con_anio.json", "w", encoding="utf-8") as f:
    json.dump(juegos, f, indent=4, ensure_ascii=False)

print("✅ Listo! Archivo guardado como steam_top_con_anio.json")