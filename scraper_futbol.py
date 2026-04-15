import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol():
    # Puedes cambiar esta URL por cualquier categoría de campeonatochileno.cl
    url = "https://www.campeonatochileno.cl/ligas/liga-de-primera-mercado-libre/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Conectando a: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscamos la tabla de posiciones
        tabla = soup.find('table')
        if not tabla:
            print("No se encontró ninguna tabla en la página.")
            return

        # 2. Mapeo dinámico de columnas (Buscamos los índices de J, DIF y PTS)
        thead = tabla.find('thead')
        headers_list = [th.get_text(strip=True).upper() for th in thead.find_all('th')]
        
        # Buscamos en qué posición están los datos que necesitamos
        try:
            idx_club = 1 # El club siempre es la segunda columna
            idx_pj = headers_list.index('J') if 'J' in headers_list else 2
            idx_dif = headers_list.index('DIF') if 'DIF' in headers_list else 8
            idx_pts = headers_list.index('PTS') if 'PTS' in headers_list else 9
            print(f"Columnas detectadas -> PJ: {idx_pj}, DIF: {idx_dif}, PTS: {idx_pts}")
        except ValueError:
            print("No se encontraron los encabezados esperados. Usando índices por defecto.")
            idx_club, idx_pj, idx_dif, idx_pts = 1, 2, 8, 9

        # 3. Extraer los datos de las filas
        standings = []
        filas = tabla.find('tbody').find_all('tr')
        
        for fila in filas:
            cols = fila.find_all('td')
            if len(cols) >= max(idx_pj, idx_dif, idx_pts):
                # Limpiamos el nombre del club (a veces traen la zona o grupo)
                nombre_raw = cols[idx_club].get_text(strip=True)
                # Si el nombre es muy largo, lo cortamos para la App
                nombre_limpio = nombre_raw.split('\n')[0].strip()

                standings.append({
                    "pos": cols[0].get_text(strip=True).replace('.', ''),
                    "club": nombre_limpio,
                    "pj": cols[idx_pj].get_text(strip=True),
                    "dg": cols[idx_dif].get_text(strip=True),
                    "pts": cols[idx_pts].get_text(strip=True)
                })

        print(f"¡Éxito! Se extrajeron {len(standings)} equipos.")

        output = {
            "fecha_actualizacion": "15 de Abril, 2026",
            "liga": "Fútbol Chileno - Tabla Actualizada",
            "standings": standings
        }

        with open('futbol_chile.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            print("Archivo futbol_chile.json actualizado.")

    except Exception as e:
        print(f"Error detectado: {str(e)}")

if __name__ == "__main__":
    scraping_futbol()
