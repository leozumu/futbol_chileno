import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol():
    # Usaremos una URL que suele ser más amigable con los scrapers
    url = "https://www.campeonatochileno.cl/ligas/liga-de-primera-mercado-libre/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        print(f"Intentando conectar con: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Respuesta del servidor: {response.status_code}")

        if response.status_code != 200:
            print("Error: El servidor bloqueó la petición.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # BUSQUEDA FLEXIBLE: Buscamos todas las tablas y filtramos la que tenga "PTS"
        tablas = soup.find_all('table')
        print(f"Tablas encontradas en la página: {len(tablas)}")
        
        target_table = None
        for t in tablas:
            texto_tabla = t.get_text().upper()
            if "PTS" in texto_tabla or "PUNTOS" in texto_tabla:
                target_table = t
                print("¡Tabla de posiciones detectada!")
                break
        
        standings = []
        if target_table:
            # Intentamos agarrar las filas tanto de tbody como de tr directos
            filas = target_table.select('tbody tr') or target_table.find_all('tr')
            
            for fila in filas:
                cols = fila.find_all(['td', 'th'])
                # Filtramos para que sean filas con datos reales (normalmente > 8 columnas)
                if len(cols) >= 9:
                    pos = cols[0].get_text(strip=True).replace('.', '')
                    # Solo procesamos si la primera columna es un número (la posición)
                    if pos.isdigit():
                        standings.append({
                            "pos": pos,
                            "club": cols[1].get_text(strip=True),
                            "pj": cols[2].get_text(strip=True),
                            "dg": cols[8].get_text(strip=True),
                            "pts": cols[9].get_text(strip=True)
                        })
        
        print(f"Total de equipos extraídos: {len(standings)}")

        # Guardar resultado
        output = {
            "fecha_actualizacion": "15 de Abril, 2026",
            "liga": "Primera División",
            "standings": standings
        }

        with open('futbol_chile.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            print("Archivo futbol_chile.json actualizado.")

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    scraping_futbol()
