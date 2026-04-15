import requests
from bs4 import BeautifulSoup
import json

def scraping_futbol():
    url = "https://www.campeonatochileno.cl/ligas/liga-de-primera-mercado-libre/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tabla = soup.find('table') # Busca la tabla de posiciones
    standings = []

    if tabla:
        filas = tabla.find('tbody').find_all('tr')
        for fila in filas:
            cols = fila.find_all('td')
            if len(cols) > 5:
                equipo = {
                    "pos": cols[0].text.strip(),
                    "club": cols[1].text.strip(),
                    "pj": cols[2].text.strip(),
                    "dg": cols[8].text.strip(),
                    "pts": cols[9].text.strip()
                }
                standings.append(equipo)

    output = {"standings": standings}
    with open('futbol_chile.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scraping_futbol()
