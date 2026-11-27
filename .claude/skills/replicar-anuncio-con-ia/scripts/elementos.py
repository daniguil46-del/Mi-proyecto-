"""Vuelve a poner encima del video los elementos que llevaba el anuncio original
(capturas de pantalla, videos insertados, emojis, flechas, carteles), en el MISMO
segundo y en el MISMO sitio, pero con el contenido de la persona.

uso:
  python3 elementos.py plantilla <carpeta>
      Deja <carpeta>/elementos.json vacio, listo para rellenar.

  python3 elementos.py montar <video.mp4> <elementos.json> [salida.mp4]
      Quema los elementos encima del video.

Cada elemento de elementos.json:
{
  "desde": 5.6,                 segundo en que aparece
  "hasta": 7.3,                 segundo en que desaparece
  "archivo": "elementos/informe.png",   png/jpg, o un mp4 para video dentro del video,
                                        o "emoji:🧪" para un emoji a color
  "x": 0.5,                     centro horizontal, de 0 a 1 (0.5 = en medio)
  "y": 0.28,                    centro vertical, de 0 a 1 (0 arriba, 1 abajo)
  "ancho": 0.92,                ancho del elemento respecto al del video
  "entrada": "fade",            fade | pop | ninguna
  "que_era": "captura del informe de PFAS"   solo para acordarse, no se usa
}

Las posiciones salen de mirar la hoja de fotogramas del original (hoja.jpg).
Todo lo que se ponga tiene que caber en la zona segura 4:5: la "y" entre 0.16 y 0.84."""
import json, os, subprocess, sys

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

def medidas(v):
    w, h = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height", "-of", "csv=p=0", v).stdout.strip().split(",")[:2]
    return int(w), int(h)

# ---------- plantilla ----------
if sys.argv[1] == "plantilla":
    carpeta = os.path.abspath(sys.argv[2])
    destino = os.path.join(carpeta, "elementos.json")
    os.makedirs(os.path.join(carpeta, "elementos"), exist_ok=True)
    ejemplo = [{
        "desde": 0.0, "hasta": 0.0,
        "archivo": "elementos/pon_aqui_tu_archivo.png",
        "x": 0.5, "y": 0.3, "ancho": 0.9, "entrada": "fade",
        "que_era": "describe que habia aqui en el original"
    }]
    json.dump(ejemplo, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Plantilla →", destino)
    print("Carpeta para los archivos →", os.path.join(carpeta, "elementos"))
    raise SystemExit

# ---------- montar ----------
VIDEO = os.path.abspath(sys.argv[2])
JSON = os.path.abspath(sys.argv[3])
SALIDA = sys.argv[4] if len(sys.argv) > 4 else os.path.splitext(VIDEO)[0] + "_ELEM.mp4"
BASE = os.path.dirname(JSON)
W, H = medidas(VIDEO)
DUR = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", VIDEO).stdout or 0)
els = [e for e in json.load(open(JSON, encoding="utf-8")) if e.get("hasta", 0) > e.get("desde", 0)]
if not els:
    raise SystemExit("elementos.json no tiene ningun elemento con 'hasta' mayor que 'desde'.")

# emojis a color: se dibujan con la fuente de Apple y se guardan como png
def emoji_png(simbolo, destino, lado=512):
    from PIL import Image, ImageDraw, ImageFont
    posibles = ["/System/Library/Fonts/Apple Color Emoji.ttc",   # Mac
                "C:/Windows/Fonts/seguiemj.ttf"]                 # Windows
    fuente = next((f for f in posibles if os.path.exists(f)), None)
    if not fuente:
        raise SystemExit("No encuentro una fuente de emojis. Usa un png en su lugar.")
    # la fuente de Apple solo admite unos pocos tamanos; se prueban de mayor a menor
    f = None
    for t in (160, 137, 96, 80, 64, 48, 32, 20):
        try:
            f = ImageFont.truetype(fuente, t); medida = t; break
        except OSError:
            continue
    if f is None:
        raise SystemExit("No se ha podido abrir la fuente de emojis. Usa un png en su lugar.")
    lienzo = int(medida * 1.6)
    im = Image.new("RGBA", (lienzo, lienzo), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((lienzo // 2, lienzo // 2), simbolo, font=f,
                            embedded_color=True, anchor="mm")
    im = im.crop(im.getbbox() or (0, 0, lienzo, lienzo))
    im = im.resize((lado, lado), Image.LANCZOS)
    im.save(destino)
    return destino

entradas, filtros, etiqueta = [f"-i", VIDEO], [], "0:v"
n_entrada = 1
tmp = []
for i, e in enumerate(els):
    arch = e["archivo"]
    if arch.startswith("emoji:"):
        destino = os.path.join(BASE, f"_emoji_{i}.png")
        arch = emoji_png(arch.split(":", 1)[1].strip(), destino)
        tmp.append(destino)
    else:
        arch = os.path.join(BASE, arch) if not os.path.isabs(arch) else arch
    if not os.path.exists(arch):
        raise SystemExit(f"No encuentro {arch}")

    es_video = arch.lower().endswith((".mp4", ".mov", ".webm", ".m4v"))
    a_, b_ = float(e["desde"]), float(e["hasta"])
    if es_video:
        entradas += ["-stream_loop", "-1", "-t", f"{b_ - a_:.3f}", "-i", arch]
    else:
        # una imagen fija se repite SOLO lo que dura el elemento. Con el filtro loop
        # infinito ffmpeg se queda sin memoria y muere sin decir nada.
        entradas += ["-loop", "1", "-t", f"{b_ - a_:.3f}", "-framerate", "30", "-i", arch]

    a, b = float(e["desde"]), float(e["hasta"])
    dur = b - a
    anchura = max(16, int(W * float(e.get("ancho", 0.5))))
    ent = e.get("entrada", "fade")
    cad = f"[{n_entrada}:v]scale={anchura}:-1"
    cad += f",trim=0:{dur:.3f},setpts=PTS-STARTPTS,format=rgba"
    if ent == "fade":
        f_in = min(0.2, dur / 3)
        cad += (f",fade=t=in:st=0:d={f_in:.3f}:alpha=1"
                f",fade=t=out:st={max(0, dur-f_in):.3f}:d={f_in:.3f}:alpha=1")
    cad += f",setpts=PTS+{a:.3f}/TB[e{i}]"
    filtros.append(cad)

    cx = f"({W}*{float(e.get('x', 0.5))}-w/2)"
    cy = f"({H}*{float(e.get('y', 0.5))}-h/2)"
    if ent == "pop":
        # un golpecito: sube un poco y baja a su sitio en los primeros 0,12 s
        cy = f"{cy}-{int(H*0.02)}*max(0,1-(t-{a:.3f})/0.12)"
    # las comas de dentro de una expresion hay que escaparlas o ffmpeg corta el filtro ahi
    cx, cy = cx.replace(",", r"\,"), cy.replace(",", r"\,")
    filtros.append(f"[{etiqueta}][e{i}]overlay=x='{cx}':y='{cy}':"
                   f"enable='between(t,{a:.3f},{b:.3f})'[v{i}]")
    etiqueta = f"v{i}"
    n_entrada += 1

orden = ["ffmpeg", "-nostdin", "-v", "error"] + entradas + [
    "-filter_complex", ";".join(filtros),
    "-map", f"[{etiqueta}]", "-map", "0:a?",
    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
    "-c:a", "copy", "-t", f"{DUR:.3f}", "-y", SALIDA]
r = subprocess.run(orden)
for f in tmp:
    os.remove(f)
if r.returncode != 0 or not os.path.exists(SALIDA):
    raise SystemExit("ffmpeg no ha podido montar los elementos.")
print(f"{len(els)} elementos montados → {SALIDA}")
