"""Cambia el formato del video sin deformar a nadie.
uso: python3 formato.py <video.mp4> <formato> [salida.mp4] [--rellenar]

  formato    9:16 | 4:5 | 1:1 | 16:9
  --rellenar en vez de recortar, deja el video entero y rellena los lados con
             el propio video desenfocado. Util cuando no quieres perder nada.

Por defecto RECORTA desde el centro, que es lo que se hace en anuncios."""
import os, subprocess, sys

args = [a for a in sys.argv[1:] if a != "--rellenar"]
RELLENAR = "--rellenar" in sys.argv
VIDEO = os.path.abspath(args[0])
FORMATO = args[1]
PROPORCIONES = {"9:16": 9 / 16, "4:5": 4 / 5, "1:1": 1.0, "16:9": 16 / 9}
if FORMATO not in PROPORCIONES:
    raise SystemExit("Formato: 9:16, 4:5, 1:1 o 16:9")
SALIDA = args[2] if len(args) > 2 else (os.path.splitext(VIDEO)[0] +
                                        "_" + FORMATO.replace(":", "x") + ".mp4")

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

w, h = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
          "stream=width,height", "-of", "csv=p=0", VIDEO).stdout.strip().split(",")[:2]
w, h = int(w), int(h)
p = PROPORCIONES[FORMATO]

# medidas estandar: 9:16 -> 1080x1920 · 4:5 -> 1080x1350 · 1:1 -> 1080x1080 · 16:9 -> 1920x1080
if p <= 1:
    AW = 1080; AH = int(round(AW / p / 2)) * 2
else:
    AW = 1920; AH = int(round(AW / p / 2)) * 2

if RELLENAR:
    filtro = (f"[0:v]scale={AW}:{AH}:force_original_aspect_ratio=increase,"
              f"crop={AW}:{AH},boxblur=40:2[fondo];"
              f"[0:v]scale={AW}:{AH}:force_original_aspect_ratio=decrease[frente];"
              f"[fondo][frente]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")
    orden = ["ffmpeg", "-nostdin", "-v", "error", "-i", VIDEO,
             "-filter_complex", filtro, "-map", "[v]", "-map", "0:a?"]
else:
    filtro = (f"scale={AW}:{AH}:force_original_aspect_ratio=increase,"
              f"crop={AW}:{AH},setsar=1")
    orden = ["ffmpeg", "-nostdin", "-v", "error", "-i", VIDEO, "-vf", filtro]
    print(f"Recorta del centro. De {w}x{h} a {AW}x{AH}: comprueba que no se corta "
          f"nada importante por los lados ni por arriba.")

orden += ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "copy", "-y", SALIDA]
if subprocess.run(orden).returncode != 0 or not os.path.exists(SALIDA):
    raise SystemExit("ffmpeg no ha podido cambiar el formato.")
print(f"{FORMATO} ({AW}x{AH}) →", SALIDA)
