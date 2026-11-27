"""Comprueba que esta todo listo antes de empezar.
uso: python3 comprobar.py"""
import os, shutil, subprocess, sys

ARCHIVO = os.path.expanduser("~/.apimart.env")
fallos = []

# 1. la clave
clave = os.environ.get("APIMART_KEY")
if not clave and os.path.exists(ARCHIVO):
    for linea in open(ARCHIVO, encoding="utf-8"):
        if linea.strip().startswith("APIMART_KEY"):
            clave = linea.split("=", 1)[1].strip().strip('"\'')
if clave:
    print(f"OK  clave de APImart encontrada (termina en ...{clave[-4:]})")
else:
    fallos.append(f"Falta la clave. Crea el archivo {ARCHIVO} con esta linea dentro:\n"
                  f"       APIMART_KEY=tu_clave_de_apimart")

# 2. ffmpeg y ffprobe
for p in ("ffmpeg", "ffprobe"):
    if shutil.which(p):
        print(f"OK  {p}")
    else:
        fallos.append(f"Falta {p}. En Mac: brew install ffmpeg")

# 3. Pillow
try:
    import PIL
    print(f"OK  Pillow {PIL.__version__}")
except ImportError:
    fallos.append("Falta Pillow. Instalalo con: pip3 install --user pillow")

print()
if fallos:
    print("FALTA ALGO:\n")
    for f in fallos:
        print("  -", f)
    sys.exit(1)
print("LISTO. Ya puedes replicar anuncios.")
