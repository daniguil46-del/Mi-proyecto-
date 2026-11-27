"""Pone el original arriba y la replica abajo, fotograma a fotograma, para revisarla.
uso: python3 comparar.py original.mp4 replica.mp4 salida.jpg [fotogramas_por_segundo]
Por defecto 2 fps. Sube a 4 si quieres mirar una union con lupa."""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

orig, repl, salida = sys.argv[1], sys.argv[2], sys.argv[3]
fps = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0

def fotogramas(v, destino):
    os.makedirs(destino, exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", v,
                    "-vf", f"fps={fps},scale=200:-2", "-y",
                    os.path.join(destino, "f%03d.jpg")], check=True)
    return sorted(os.path.join(destino, f) for f in os.listdir(destino))

with tempfile.TemporaryDirectory() as tmp:
    a = fotogramas(orig, os.path.join(tmp, "o"))
    b = fotogramas(repl, os.path.join(tmp, "r"))
    n = min(len(a), len(b))
    CW, CH = 200, 356
    hoja = Image.new("RGB", (n * CW, 2 * (CH + 20)), "white")
    d = ImageDraw.Draw(hoja)
    for i in range(n):
        hoja.paste(Image.open(a[i]), (i * CW, 20))
        hoja.paste(Image.open(b[i]), (i * CW, CH + 40))
        d.text((i * CW + 3, 4), f"{i/fps:.1f}s", fill="black")
        d.text((i * CW + 3, CH + 24), "REPLICA", fill="red")
    hoja.save(salida, quality=85)

print(salida)
print("Mira, en este orden: 1) la persona es la misma, 2) el producto esta en el estado correcto,")
print("3) no falta ninguna mano ni objeto que si esta en el original, 4) no hay texto,")
print("5) el ultimo plano existe. Repite SOLO el trozo que falle.")
