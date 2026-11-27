"""Analiza el anuncio: detecta los cortes, propone los trozos y saca una hoja de fotogramas.
uso: python3 preparar.py <carpeta> [umbral]
El umbral por defecto es 0.06. NO lo subas a 0.3: con ese valor no detecta nada en los
anuncios tipo UGC, donde los cortes son entre planos parecidos de la misma persona.
Deja <carpeta>/cortes.json, <carpeta>/tramos.json, <carpeta>/hoja.jpg y los <carpeta>/tramoN.mp4"""
import json, os, re, subprocess, sys

MAX = 15.0   # Wan 3.0 no acepta mas de 15 s por tirada
carpeta = os.path.abspath(sys.argv[1])
UMBRAL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.06
video = os.path.join(carpeta, "viral_full.mp4")

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", video).stdout.strip())
w, h = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
          "stream=width,height", "-of", "csv=p=0", video).stdout.strip().split(",")
print(f"Duracion {dur:.2f} s · {w}x{h}")

# --- cortes de plano ---
sal = sh("ffmpeg", "-v", "info", "-i", video, "-vf",
         f"select='gt(scene,{UMBRAL})',showinfo", "-an", "-f", "null", "-").stderr
cortes = sorted({round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", sal)})
# quita cortes pegados (menos de 0,4 s) y los de los extremos
limpios = []
for c in cortes:
    if c < 0.5 or c > dur - 0.5:
        continue
    if limpios and c - limpios[-1] < 0.4:
        continue
    limpios.append(c)
print(f"Cortes de plano (umbral {UMBRAL}): {limpios}")
if not limpios:
    print("  No ha detectado ningun corte. Si el anuncio si los tiene, repite bajando")
    print("  el umbral:  python3 preparar.py <carpeta> 0.04")

# --- trozos: los MENOS posibles, sin pasarse de MAX y cortando en un corte real ---
puntos = limpios + [round(dur, 2)]
tramos, ini = [], 0.0
while dur - ini > 0.2:
    caben = [c for c in puntos if ini < c <= ini + MAX]
    fin = max(caben) if caben else round(min(ini + MAX, dur), 2)
    tramos.append((round(ini, 2), fin))
    ini = fin

# el audio original, cortado igual que los trozos: va a Wan como referencia de voz
# (asi copia la misma voz y las mismas palabras, y la boca cuadra)
tiene_voz = bool(sh("ffprobe", "-v", "error", "-select_streams", "a:0",
                    "-show_entries", "stream=codec_type", "-of", "csv=p=0", video).stdout.strip())
dir_audio = os.path.join(carpeta, "audios")
if tiene_voz:
    os.makedirs(dir_audio, exist_ok=True)
else:
    print("El anuncio no lleva audio: no se puede usar voz de referencia.")

info = []
for i, (a, b) in enumerate(tramos, 1):
    n = f"tramo{i}"
    sh("ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-i", video, "-t", str(round(b - a, 2)),
       "-an", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-y", os.path.join(carpeta, n + ".mp4"))
    if tiene_voz:
        # Wan acepta como maximo 15 s de audio de referencia
        sh("ffmpeg", "-nostdin", "-v", "error", "-ss", str(a), "-i", video,
           "-t", str(min(round(b - a, 2), 15.0)), "-vn", "-ac", "1", "-ar", "44100",
           "-b:a", "128k", "-y", os.path.join(dir_audio, n + ".mp3"))
    seg = round(b - a, 2)
    info.append({"nombre": n, "desde": a, "hasta": b, "dur": seg, "dur_api": int(seg) + (1 if seg % 1 else 0)})
    print(f"  {n}  {a:6.2f}–{b:<6.2f}  {seg:5.2f} s  → se pide a la API {info[-1]['dur_api']} s")

json.dump(limpios, open(os.path.join(carpeta, "cortes.json"), "w"), indent=2)
json.dump(info, open(os.path.join(carpeta, "tramos.json"), "w"), indent=2)
total = sum(t["dur_api"] for t in info)
print(f"\n{len(info)} trozos · {total} s a generar · coste aproximado {total*0.066:.2f} $ por pasada")
if tiene_voz:
    print(f"Audio de referencia listo en {dir_audio} (un mp3 por trozo).")

# --- hoja de fotogramas, 1 por segundo ---
from PIL import Image, ImageDraw
tmp = os.path.join(carpeta, "_hoja")
os.makedirs(tmp, exist_ok=True)
sh("ffmpeg", "-nostdin", "-v", "error", "-i", video, "-vf", "fps=1,scale=150:-2",
   "-y", os.path.join(tmp, "f%03d.jpg"))
fs = sorted(os.listdir(tmp))
COLS, CW, CH = 13, 150, 267
filas = (len(fs) + COLS - 1) // COLS
hoja = Image.new("RGB", (COLS * CW, filas * (CH + 18)), "white")
d = ImageDraw.Draw(hoja)
for i, f in enumerate(fs):
    im = Image.open(os.path.join(tmp, f))
    hoja.paste(im, ((i % COLS) * CW, (i // COLS) * (CH + 18) + 18))
    d.text(((i % COLS) * CW + 3, (i // COLS) * (CH + 18) + 3), f"{i}s", fill="black")
hoja.save(os.path.join(carpeta, "hoja.jpg"), quality=85)
for f in fs:
    os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
print("Hoja de fotogramas →", os.path.join(carpeta, "hoja.jpg"))
