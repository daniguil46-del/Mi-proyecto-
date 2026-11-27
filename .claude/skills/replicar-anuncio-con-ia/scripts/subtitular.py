"""Pone los subtitulos quemados en el video ya montado.
uso: python3 subtitular.py <video.mp4> [idioma] [estilo] [--clave palabra,palabra,...]

  idioma   codigo de dos letras del audio (en, es, fr...) o "auto". Decirlo mejora la precision.
  estilo   original (por defecto) | limpio
             original -> una palabra cada vez, blanca con sombra, en el centro-bajo,
                         y las palabras clave en AMARILLO. Es el estilo de los anuncios UGC.
             limpio   -> grupos de 3 palabras, blanco con borde negro, abajo. Sin animacion.
  --clave  las palabras que van en amarillo (solo en el estilo original). Van las que
           sostienen el anuncio: el producto, el problema y los numeros.
           Ejemplo:  --clave bleach,PFAS,formaldehyde,soft,strong

Transcribe con Whisper-1 de APImart, que va con la MISMA clave que ya tienes: el alumno no
instala nada mas. Deja el .srt y el .ass al lado por si hay que retocar algo a mano, y los
subtitulos van dentro de la zona segura 4:5 (no los tapa ni Instagram ni TikTok)."""
import os, re, subprocess, sys

args = sys.argv[1:]
clave_palabras = []
if "--clave" in args:
    i = args.index("--clave")
    clave_palabras = [w.strip().lower() for w in args[i + 1].split(",") if w.strip()]
    del args[i:i + 2]

VIDEO = os.path.abspath(args[0])
IDIOMA = args[1] if len(args) > 1 and args[1] not in ("-", "auto") else None
ESTILO = args[2] if len(args) > 2 else "original"
BASE = os.path.splitext(VIDEO)[0]

clave = os.environ.get("APIMART_KEY")
env = os.path.expanduser("~/.apimart.env")
if not clave and os.path.exists(env):
    m = re.search(r'APIMART_KEY="?([^"\n]+)', open(env, encoding="utf-8").read())
    clave = m.group(1).strip() if m else None
if not clave:
    raise SystemExit(f"Falta la clave. Ponla en {env} asi:  APIMART_KEY=tu_clave")

def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)

def para_filtro(ruta):
    """En un filtro de ffmpeg, una ruta de Windows (C:\\carpeta) revienta: la barra
    invertida escapa y los dos puntos separan opciones. Hay que darle la vuelta."""
    r = ruta.replace("\\", "/")
    return r.replace(":", "\\:")

# 1 · audio en mp3 (el limite de Whisper son 25 MB)
audio = BASE + "_audio.mp3"
sh("ffmpeg", "-nostdin", "-v", "error", "-i", VIDEO, "-vn", "-ac", "1",
   "-ar", "16000", "-b:a", "64k", "-y", audio)
if not os.path.exists(audio):
    raise SystemExit("No se ha podido sacar el audio del video.")
if os.path.getsize(audio) > 25 * 1024 * 1024:
    raise SystemExit("El audio pasa de 25 MB. Corta el video en dos y subtitula por partes.")
print(f"Audio {os.path.getsize(audio)/1024/1024:.1f} MB")

# 2 · transcribir
orden = ["curl", "-s", "--max-time", "300",
         "https://api.apimart.ai/v1/audio/transcriptions",
         "-H", f"Authorization: Bearer {clave}",
         "-F", f"file=@{audio}", "-F", "model=whisper-1", "-F", "response_format=srt"]
if IDIOMA:
    orden += ["-F", f"language={IDIOMA}"]
srt = sh(*orden).stdout.strip()
os.remove(audio)
if not srt or srt.lstrip().startswith("{"):
    raise SystemExit(f"La transcripcion ha fallado:\n{srt[:400]}")
print("Transcrito.")

def a_seg(t):
    h, m, resto = t.split(":")
    s, ms = resto.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

frases = []
for b in [x for x in re.split(r"\n\s*\n", srt) if x.strip()]:
    lineas = [l for l in b.strip().split("\n") if l.strip()]
    tiempo = next((l for l in lineas if "-->" in l), None)
    if not tiempo:
        continue
    ini, fin = [a_seg(x.strip()) for x in tiempo.split("-->")]
    texto = " ".join(lineas[lineas.index(tiempo) + 1:]).strip()
    if texto:
        frases.append((ini, fin, texto))

# Whisper devuelve la frase entera, no palabra a palabra. Repartimos el hueco entre las
# palabras segun lo que mide cada una, que suena mas natural que partirlo en trozos iguales.
def repartir(ini, fin, palabras):
    pesos = [max(len(p), 2) for p in palabras]
    total = sum(pesos)
    t, salida = ini, []
    for p, w in zip(palabras, pesos):
        d = (fin - ini) * w / total
        salida.append((t, t + d, p))
        t += d
    return salida

alto = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
          "stream=height", "-of", "csv=p=0", VIDEO).stdout.strip()
alto = int(alto) if alto.isdigit() else 1920
ancho = sh("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
           "stream=width", "-of", "csv=p=0", VIDEO).stdout.strip()
ancho = int(ancho) if ancho.isdigit() else 1080

def a_ass(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"

def limpia(p):
    return re.sub(r"[^\w']", "", p).lower()

if ESTILO == "original":
    cuerpo, margen = int(alto * 0.055), int(alto * 0.33)
    sombra = max(2, int(alto * 0.002))
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {ancho}
PlayResY: {alto}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Blanca,Arial,{cuerpo},&H00FFFFFF,&H000000FF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,{sombra},{sombra},2,40,40,{margen},1
Style: Amarilla,Arial,{cuerpo},&H0000D6FF,&H000000FF,&H00202020,&H80000000,-1,0,0,0,100,100,0,0,1,{sombra},{sombra},2,40,40,{margen},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    filas, n = [], 0
    for ini, fin, texto in frases:
        for a, b, p in repartir(ini, fin, texto.split()):
            est = "Amarilla" if limpia(p) in clave_palabras else "Blanca"
            # un golpecito de escala al entrar, como los anuncios
            efecto = r"{\fscx85\fscy85\t(0,90,\fscx100\fscy100)}"
            filas.append(f"Dialogue: 0,{a_ass(a)},{a_ass(b)},{est},,0,0,0,,{efecto}{p}")
            n += 1
    ass = BASE + ".ass"
    open(ass, "w", encoding="utf-8").write(cab + "\n".join(filas) + "\n")
    print(f"{n} palabras · {len(clave_palabras)} en amarillo → {ass}")
    filtro = f"ass={para_filtro(ass)}"
else:
    cuerpo, margen = int(alto * 0.034), int(alto * 0.21)
    trozos, n = [], 0
    for ini, fin, texto in frases:
        pal = texto.split()
        grupos = [pal[i:i + 3] for i in range(0, len(pal), 3)]
        paso = (fin - ini) / len(grupos)
        for i, g in enumerate(grupos):
            trozos.append((ini + i * paso, ini + (i + 1) * paso, " ".join(g)))
    def a_srt(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = int(x % 60)
        return f"{h:02d}:{m:02d}:{s:02d},{int(round((x-int(x))*1000)):03d}"
    srt_out = BASE + ".srt"
    with open(srt_out, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(trozos, 1):
            f.write(f"{i}\n{a_srt(a)} --> {a_srt(b)}\n{t}\n\n")
    print(f"{len(trozos)} subtitulos → {srt_out}")
    estilo = (f"FontName=Arial,Fontsize={int(cuerpo*0.63)},Bold=1,PrimaryColour=&H00FFFFFF,"
              f"OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=1,"
              f"Alignment=2,MarginV={margen}")
    filtro = f"subtitles={para_filtro(srt_out)}:force_style='{estilo}'"

# guardar siempre el srt de frases, por si hay que corregir una palabra
plano = BASE + "_texto.srt"
with open(plano, "w", encoding="utf-8") as f:
    for i, (a, b, t) in enumerate(frases, 1):
        f.write(f"{i}\n{a_ass(a)} --> {a_ass(b)}\n{t}\n\n")

final = BASE + "_SUB.mp4"
r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", VIDEO,
                    "-vf", filtro, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-c:a", "copy", "-y", final])
if r.returncode != 0 or not os.path.exists(final):
    raise SystemExit("ffmpeg no ha podido quemar los subtitulos.")
print("\nListo →", final)
