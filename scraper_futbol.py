import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol_final():
    # URL de ESPN Chile (La fuente más estable para scraping estático)
    url = "https://www.espn.cl/futbol/posiciones/_/liga/chi.1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Analizando fuente de datos: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        
        # 1. Ubicamos la tabla de Nombres (Fixed Left)
        table_names = soup.find('table', class_='Table--fixed-left')
        # 2. Ubicamos la tabla de Estadísticas (Scroller)
        table_stats = soup.find('div', class_='Table__Scroller').find('table')

        if table_names and table_stats:
            # Extraemos las filas de ambas (saltando el encabezado)
            rows_names = table_names.find('tbody').find_all('tr')
            rows_stats = table_stats.find('tbody').find_all('tr')

            for i in range(len(rows_names)):
                # --- Lógica para la Tabla de Nombres ---
                pos = rows_names[i].find('span', class_='team-position').get_text(strip=True)
                # Buscamos el nombre en el span que no es para mobile para que salga completo
                nombre = rows_names[i].find('span', class_='hide-mobile').get_text(strip=True)
                
                # --- Lógica para la Tabla de Números ---
                cols = rows_stats[i].find_all('td')
                
                # Según el código fuente que enviaste, el orden es:
                # [0]GP (PJ), [1]W, [2]D, [3]L, [4]GF, [5]GA, [6]GD (DG), [7]P (PTS)
                pj = cols[0].get_text(strip=True)
                dg = cols[6].get_text(strip=True)
                pts = cols[7].get_text(strip=True)

                standings.append({
                    "pos": pos,
                    "club": nombre,
                    "pj": pj,
                    "dg": dg,
                    "pts": pts
                })

            print(f"✅ ¡Proceso exitoso! {len(standings)} equipos sincronizados.")
        else:
            print("❌ No se detectó la estructura de tablas esperada.")

        # Guardamos el archivo final para tu WebApp
        output = {
            "fecha_actualizacion": "15 de Abril, 2026",
            "liga": "Primera División de Chile",
            "standings": standings
        }

        with open('futbol_chile.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            print("📂 Archivo 'futbol_chile.json' generado con éxito.")

    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")

if __name__ == "__main__":
    scraping_futbol_final()
