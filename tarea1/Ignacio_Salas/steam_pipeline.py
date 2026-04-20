import json
import requests
import time
import pandas as pd

# ==============================
# CONFIG
# ==============================
INPUT_FILE = "steam_top.json"
OUTPUT_JSON = "steam_top_enriquecido.json"
OUTPUT_CSV = "steam_top_enriquecido.csv"

SLEEP_TIME = 1.2  # evita bloqueos de Steam

# ==============================
# FUNCIONES API
# ==============================

def get_game_data(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=spanish"
    
    try:
        res = requests.get(url)
        data = res.json()

        if not data[str(appid)]["success"]:
            return {}

        game = data[str(appid)]["data"]

        return {
            "desarrollador": game.get("developers", ["N/A"])[0] if game.get("developers") else None,
            "precio_actual": game.get("price_overview", {}).get("final_formatted", "Free/N/A"),
            "descripcion": game.get("short_description"),
            "generos": ", ".join([g["description"] for g in game.get("genres", [])]),
            "nota_metacritic": game.get("metacritic", {}).get("score", None)
        }

    except Exception as e:
        print(f"Error appdetails {appid}: {e}")
        return {}


def get_reviews(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1"

    try:
        res = requests.get(url)
        data = res.json()

        summary = data.get("query_summary", {})

        return {
            "porcentaje_reseñas_positivas": summary.get("review_score_desc"),
        }

    except Exception as e:
        print(f"Error reviews {appid}: {e}")
        return {}


# ==============================
# MAIN
# ==============================

def main():
    # 🔹 cargar JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        juegos = json.load(f)

    total = len(juegos)
    print(f"Procesando {total} juegos...\n")

    for i, juego in enumerate(juegos, 1):
        appid = juego["appid"]
        nombre = juego["nombre"]

        print(f"[{i}/{total}] {nombre} ({appid})")

        # 🔹 obtener datos
        data = get_game_data(appid)
        reviews = get_reviews(appid)

        # 🔹 actualizar
        juego.update(data)
        juego.update(reviews)

        # 🔹 pausa
        time.sleep(SLEEP_TIME)

    # ==============================
    # GUARDAR JSON
    # ==============================
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(juegos, f, ensure_ascii=False, indent=4)

    print(f"\nJSON guardado en {OUTPUT_JSON}")

    # ==============================
    # GUARDAR CSV
    # ==============================
    df = pd.DataFrame(juegos)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"CSV guardado en {OUTPUT_CSV}")


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()