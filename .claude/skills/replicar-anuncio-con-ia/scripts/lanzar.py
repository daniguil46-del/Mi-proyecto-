"""Manda los trozos a Wan 3.0 (APImart) y baja los resultados.
uso: python3 lanzar.py <carpeta>/rondaN
rondaN/pruebas.json = [{"nombre","video","duracion","prompt","ref"?}]
   "video" y "ref" van relativos a <carpeta>.  "ref" es la foto del avatar (opcional).
Apunta cada task_id en rondaN/task_ids.txt NADA MAS lanzarlo: una tarea perdida es un video
pagado que no se recupera."""
import json, os, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ARCHIVO = os.path.expanduser("~/.apimart.env")
K = os.environ.get("APIMART_KEY")
if not K:
    K = re.search(r'APIMART_KEY\s*=\s*"?([^"\n]+)', open(ARCHIVO).read()).group(1)
API = "https://api.apimart.ai/v1"
RONDA = os.path.abspath(sys.argv[1])
BASE = os.path.dirname(RONDA)

def api(ruta, cuerpo=None):
    r = urllib.request.Request(API + ruta,
        data=json.dumps(cuerpo).encode() if cuerpo else None,
        method="POST" if cuerpo else "GET",
        headers={"Authorization": f"Bearer {K}", "Content-Type": "application/json"})
    for _ in range(30):
        try:
            return json.loads(urllib.request.urlopen(r, timeout=60).read())
        except urllib.error.HTTPError as e:
            return {"http_error": e.code, "body": e.read().decode()[:800]}
        except Exception:
            time.sleep(20)
    return {"error": "sin conexion"}

def subir(f):
    """uguu.se: alojamiento publico temporal (24 h). La API necesita una URL, no un archivo."""
    for _ in range(5):
        r = subprocess.run(["curl", "-s", "-F", f"files[]=@{f}", "https://uguu.se/upload"],
                           capture_output=True, text=True)
        try:
            return json.loads(r.stdout)["files"][0]["url"]
        except Exception:
            time.sleep(10)
    raise SystemExit("No se pudo subir el archivo. Vuelve a intentarlo: uguu.se falla de vez en cuando.")

def correr(p):
    cuerpo = {"model": "wan3.0-video", "prompt": p["prompt"],
              "video_urls": [subir(os.path.join(BASE, p["video"]))],
              "resolution": "480P",      # SIN esto cobra 1080P, que cuesta el cuadruple
              "size": "9:16", "duration": p["duracion"], "audio": True}
    # voz de referencia: el trozo de audio del original que le toca a este tramo.
    # Con esto Wan copia la misma voz y dice las mismas palabras, y la boca cuadra.
    aud = p.get("audio") or os.path.join("audios", p["nombre"] + ".mp3")
    if os.path.exists(os.path.join(BASE, aud)):
        cuerpo["audio_urls"] = [subir(os.path.join(BASE, aud))]
    if p.get("ref"):
        cuerpo["image_urls"] = [subir(os.path.join(BASE, p["ref"]))]
    r = api("/videos/generations", cuerpo)
    t0 = time.time(); out = dict(p)
    if r.get("http_error") == 402:
        print("SIN SALDO: recarga en apimart.ai", flush=True)
    try:
        tid = r["data"][0]["task_id"]
    except Exception:
        out["error"] = r
        print(p["nombre"], "ERROR", r, flush=True)
        return out
    out["task_id"] = tid
    print(p["nombre"], "task_id:", tid, flush=True)
    open(os.path.join(RONDA, "task_ids.txt"), "a").write(f"{p['nombre']} {tid}\n")
    while True:
        time.sleep(10)
        d = api(f"/tasks/{tid}"); d = d.get("data", d); st = d.get("status")
        if st in ("completed", "failed", "error", "cancelled") or time.time() - t0 > 1800:
            break
    out.update({"estado": st, "segundos": round(time.time() - t0),
                "creditos": d.get("credits_cost"), "error": d.get("error")})
    try:
        u = d["result"]["videos"][0]["url"]
        u = u[0] if isinstance(u, list) else u
        out["archivo"] = p["nombre"] + ".mp4"
        urllib.request.urlretrieve(u, os.path.join(RONDA, out["archivo"]))
    except Exception as e:
        out["error_descarga"] = str(e)[:200]
    print(p["nombre"], st, out["segundos"], "s · creditos", out.get("creditos"),
          out.get("error") or "", flush=True)
    return out

P = json.load(open(os.path.join(RONDA, "pruebas.json")))
with ThreadPoolExecutor(len(P)) as ex:
    res = list(ex.map(correr, P))
json.dump(res, open(os.path.join(RONDA, "resultados.json"), "w"), ensure_ascii=False, indent=2)
t = sum((x.get("creditos") or 0) for x in res)
print(f"\nTOTAL: {t:.2f} creditos = {t*0.1:.2f} $")
