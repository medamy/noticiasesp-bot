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
nombre_archivo = f"videos/video_{int(time.time())}.mp4"

while True:
s = requests.get(f"https://api.creatomate.com/v1/renders/{rid}",
headers={"Authorization": f"Bearer {API}"}).json()
print("Estado:", s["status"])
if s["status"] == "succeeded":
open(nombre_archivo, "wb").write(requests.get(s["url"]).content)
print(f"Video guardado: {nombre_archivo}")
break
elif s["status"] == "failed":
print("Error al generar video")
break
time.sleep(5)

TIKTOK_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN")
if TIKTOK_TOKEN:
print("Subiendo a TikTok...")
with open(nombre_archivo, "rb") as f:
video_data = f.read()
headers = {"Authorization": f"Bearer {TIKTOK_TOKEN}"}
init = requests.post("https://open.tiktokapis.com/v2/post/publish/video/init/",
headers=headers,
json={"post_info": {"title": noticias[0][:150], "privacy_level": "PUBLIC_TO_EVERYONE"},
"source_info": {"source": "FILE_UPLOAD", "video_size": len(video_data), "chunk_size": len(video_data), "total_chunk_count": 1}})
data = init.json()
upload_url = data.get("data", {}).get("upload_url")
if upload_url:
requests.put(upload_url, data=video_data, headers={"Content-Type": "video/mp4"})
print("Video subido a TikTok!")
else:
print("Error TikTok:", data)
else:
print("Sin token TikTok - video guardado localmente.")
