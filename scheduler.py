import subprocess
import time
from datetime import datetime
import pytz

ZONA = pytz.timezone("Europe/Madrid")
HORAS_EJECUCION = [11]
ejecuciones_realizadas = set()

print("Scheduler iniciado. Esperando horas programadas...")

while True:
    ahora = datetime.now(ZONA)
    clave = (ahora.date(), ahora.hour)
    if ahora.hour in HORAS_EJECUCION and clave not in ejecuciones_realizadas:
        print(f"{ahora.strftime('%Y-%m-%d %H:%M')} Generando video...")
        subprocess.run(["python", "video.py"])
        ejecuciones_realizadas.add(clave)
    time.sleep(30)
