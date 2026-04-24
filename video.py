import requests
import xml.etree.ElementTree as ET
import os
import time

API = os.environ.get("CREATOMATE_API_KEY")
TID = os.environ.get("TEMPLATE_ID")

os.makedirs("videos", exist_ok=True)

print("Obteniendo noticias de El País...")
rss = requests.get("https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada", timeout=10)
root = ET.fromstring(rss.content)
items = root.findall(".//item")
noticias = [item.find("title").text for item in items[:3] if item.find("title") is not None]

while len(noticias) < 3:
    noticias.append(f"Noticia {len(noticias) + 1}")

print("Noticias:", noticias)

r = requests.post("https://api.creatomate.com/v1/renders",
    headers={"Authorization": f"Bearer {API}", "Content-Type": "application/json"},
    json={"template_id": TID, "modifications": {
        "Title": "Noticias del dia",
        "Slide-1-Text": noticias[0],
        "Slide-2-Text": noticias[1],
        "Slide-3-Text": noticias[2]
    }})

rid = r.json()[0]["id"]
print(f"Render iniciado: {rid}")

for _ in range(30):
    time.sleep(10)
    s = requests.get(f"https://api.creatomate.com/v1/renders/{rid}",
        headers={"Authorization": f"Bearer {API}"})
    estado = s.json()["status"]
    print(f"Estado: {estado}")
    if estado == "succeeded":
        url = s.json()["url"]
        print(f"Video listo: {url}")
        break
