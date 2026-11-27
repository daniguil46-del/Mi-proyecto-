"""Baja el anuncio que vamos a replicar.
uso: python3 bajar.py "<enlace de TrendTrack | URL de un .mp4 | ruta a un .mp4>" <carpeta>
Deja <carpeta>/viral_full.mp4 y, si viene de TrendTrack, <carpeta>/ficha.json"""
import json, os, re, shutil, sys, urllib.request

# Sin cabeceras de navegador la API de TrendTrack contesta 403.
CABECERAS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://app.trendtrack.io",
    "Referer": "https://app.trendtrack.io/",
}

def abrir(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=CABECERAS), timeout=120)

origen, carpeta = sys.argv[1], sys.argv[2]
os.makedirs(carpeta, exist_ok=True)
destino = os.path.join(carpeta, "viral_full.mp4")
ficha = {}

m = re.search(r"share/ad/([A-Za-z0-9_\-]+)", origen)
if m:
    d = json.loads(abrir(f"https://app-api.trendtrack.io/api/v1/explorer/share/ads/{m.group(1)}").read())
    a = d.get("metaAd") or d
    ficha = {k: a.get(k) for k in ("advertiserName", "siteName", "daysRunning", "mediaDuration",
                                   "mediaUrl", "description", "landingUrl", "duplicates")}
    origen = ficha["mediaUrl"]

if origen.startswith("http"):
    with abrir(origen) as r, open(destino, "wb") as f:
        shutil.copyfileobj(r, f)
else:
    shutil.copyfile(os.path.expanduser(origen), destino)

if ficha:
    json.dump(ficha, open(os.path.join(carpeta, "ficha.json"), "w"), ensure_ascii=False, indent=2)
    for k, v in ficha.items():
        if k != "description":
            print(f"{k}: {v}")
    print("Copy:", (ficha.get("description") or "")[:300])

print(f"\nGuardado en {destino}  ({os.path.getsize(destino)/1e6:.1f} MB)")
