import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol():
    # URL de ESPN Chile (Primera División) - Muy amigable para scraping
    url = "https://www.espn.cl/futbol/posiciones/_/liga/chi.1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Conectando a fuente alternativa (ESPN): {url}")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ESPN separa los nombres de los equipos de las estadísticas en dos tablas
        # Vamos a unirlas de forma inteligente
        standings = []
        
        # 1. Obtenemos los nombres y posiciones
        table_teams = soup.find('table', class_='Table--fixed-left')
        # 2. Obtenemos las estadísticas (PJ, DG, PTS)
        table_stats = soup.find('div', class_='Table__Scroller').find('table') if soup.find('div', class_='Table__Scroller') else None

        if table_teams and table_stats:
            rows_teams = table_teams.find_all('tr')[1:] # Saltamos el encabezado
            rows_stats = table_stats.find_all('tr')[1:] # Saltamos el encabezado

            for i in range(len(rows_teams)):
                # Datos del equipo
                pos = rows_teams[i].find('span', class_='team-position').get_text(strip=True)
                nombre = rows_teams[i].find('span', class_='hide-mobile').get_text(strip=True)
                
                # Datos de estadísticas
                cols_stats = rows_stats[i].find_all('td')
                pj = cols_stats[0].get_text(strip=True)
                dg = cols_stats[7].get_text(strip=True) # ESPN usa la columna 7 para Dif Goles
                pts = cols_stats[8].get_text(strip=True) # ESPN usa la columna 8 para Puntos

                standings.append({
                    "pos": pos,
                    "club": nombre,
                    "pj": pj,
                    "dg": dg,
                    "pts": pts
                })

        print(f"¡Éxito! Se extrajeron {len(standings)} equipos.")

        output = {
            "fecha_actualizacion": "15 de Abril, 2026",
            "liga": "Primera División de Chile",
            "fuente": "ESPN / DUPLOS.CL",
            "standings": standings
        }

        with open('futbol_chile.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            print("Archivo futbol_chile.json actualizado con éxito.")

    except Exception as e:
        print(f"Error en el proceso: {str(e)}")

if __name__ == "__main__":
    scraping_futbol()
