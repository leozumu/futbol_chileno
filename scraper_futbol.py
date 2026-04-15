import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol():
    # URL oficial de Primera División
    url = "https://www.campeonatochileno.cl/ligas/liga-de-primera-mercado-libre/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos la tabla con la clase específica que usa la ANFP
        tabla = soup.find('table', class_='table-hover')
        standings = []

        if tabla:
            # Buscamos todas las filas de datos (tr) dentro del cuerpo (tbody)
            filas = tabla.find('tbody').find_all('tr')
            
            for fila in filas:
                cols = fila.find_all('td')
                
                # Verificamos que la fila tenga las columnas suficientes
                if len(cols) >= 10:
                    equipo = {
                        "pos": cols[0].get_text(strip=True),
                        "club": cols[1].get_text(strip=True),
                        "pj": cols[2].get_text(strip=True),
                        "dg": cols[8].get_text(strip=True), # Diferencia de Goles
                        "pts": cols[9].get_text(strip=True)  # Puntos
                    }
                    standings.append(equipo)
        
        # Si standings sigue vacío, imprimimos para el log de GitHub
        if not standings:
            print("No se encontraron datos en la tabla.")

        output = {
            "fecha_actualizacion": "15 de Abril, 2026",
            "liga": "Primera División",
            "standings": standings
        }

        with open('futbol_chile.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error durante el scraping: {e}")

if __name__ == "__main__":
    scraping_futbol()
