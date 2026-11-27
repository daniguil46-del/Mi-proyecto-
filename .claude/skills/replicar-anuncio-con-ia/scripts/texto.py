"""Hace un PNG con un texto, para ponerlo encima del video con elementos.py.
uso: python3 texto.py "Linea 1|Linea 2 😍" salida.png [--estilo caja|limpio] [--ancho 900]

  |        separa las lineas
  caja     texto negro sobre caja blanca redondeada. El estilo mas usado en anuncios
  limpio   texto blanco con borde negro, sin caja

Los emojis salen a color en Mac."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

args = sys.argv[1:]
def saca(nombre, por_defecto):
    if nombre in args:
        i = args.index(nombre); v = args[i + 1]; del args[i:i + 2]; return v
    return por_defecto

ESTILO = saca("--estilo", "caja")
ANCHO = int(saca("--ancho", "900"))
TEXTO, SALIDA = args[0], os.path.abspath(args[1])
lineas = [l.strip() for l in TEXTO.split("|") if l.strip()]

FUENTES = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
           "/System/Library/Fonts/Helvetica.ttc",
           "C:/Windows/Fonts/arialbd.ttf"]
ruta = next((f for f in FUENTES if os.path.exists(f)), None)
if not ruta:
    raise SystemExit("No encuentro una fuente. Pasa una ruta de .ttf en el codigo.")

CUERPO = int(ANCHO * 0.085)
f = ImageFont.truetype(ruta, CUERPO)
emoji = None
re_emoji = next((f for f in ["/System/Library/Fonts/Apple Color Emoji.ttc",
                            "C:/Windows/Fonts/seguiemj.ttf"] if os.path.exists(f)), "")
if re_emoji:
    for t in (160, 137, 96, 64, 48):
        try:
            emoji = ImageFont.truetype(re_emoji, t); break
        except OSError:
            continue

tmp = Image.new("RGBA", (10, 10)); d = ImageDraw.Draw(tmp)
anchos = [d.textbbox((0, 0), l, font=f)[2] for l in lineas]
alto_l = int(CUERPO * 1.35)
pad = int(CUERPO * 0.55)
W = max(anchos) + pad * 2
H = alto_l * len(lineas) + pad * 2

im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
if ESTILO == "caja":
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=int(pad * 0.9), fill=(255, 255, 255, 240))
    color, borde = (18, 18, 18, 255), None
else:
    color, borde = (255, 255, 255, 255), (0, 0, 0, 255)

for i, l in enumerate(lineas):
    x = (W - anchos[i]) // 2
    y = pad + i * alto_l
    if borde:
        d.text((x, y), l, font=f, fill=color, stroke_width=max(2, CUERPO // 14),
               stroke_fill=borde, embedded_color=True)
    else:
        d.text((x, y), l, font=f, fill=color, embedded_color=True)

im.save(SALIDA)
print(f"{W}x{H} →", SALIDA)
